package System_Design_Interview

import (
	"strconv"

	"github.com/go-redis/redis"
	"github.com/spf13/viper"
)

func checkSmsSentExceedByIp(ip string) error {
	fastlog.Infof("Check ip:%s sms sent times", ip)

	key := constvar.DefaultSmsSentIpRedisPrefixKey + ip
	pipe := rc.RedisClient.Self.Pipeline()
	defer pipe.Close()

	val, err := rc.RedisClient.Self.Get(key).Result()
	if err != nil {
		if err == redis.Nil {
			pipe.Incr(key)
			pipe.Expire(key, constvar.DefaultSmsRedisKeyExpireTime)
			if _, err := pipe.Exec(); err != nil {
				fastlog.Errorf("Redis hincrby %s failed: %s", key, err)
				return err
			}
			return nil
		}
		fastlog.Errorf("Get redis key: %s failed: %s", key, err)
		return err
	}

	index, err := strconv.Atoi(val)
	if err != nil {
		fastlog.Errorf("Convert value: %s to int failed: %s", val, err)
		return err
	}

	if index >= viper.GetInt("redis.sms_sent_ip_max_num") {
		fastlog.Infoln("Sent sms code exceed times by ip")
		return errors.New("sent sms code exceed times by ip")
	}
	pipe.Incr(key)
	pipe.Expire(key, constvar.DefaultSmsRedisKeyExpireTime)
	if _, err := pipe.Exec(); err != nil {
		fastlog.Errorf("Redis hincrby %s failed: %s", key, err)
		return err
	}
	return nil
}
