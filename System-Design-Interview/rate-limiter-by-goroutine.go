package System_Design_Interview

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type RateLimiter struct {
	Limit    int
	Duration time.Duration
}

func rateLimitMiddleware(limiters map[string]*RateLimiter) gin.HandlerFunc {
	return func(c *gin.Context) {
		// Extract relevant information from the context
		key := c.ClientIP() // You can also use user ID or path for finer control
		limiter, ok := limiters[key]

		if !ok {
			// No limit defined for this key, continue processing
			c.Next()
			return
		}

		// Check rate limit using a counter stored in context
		counter, exists := c.Get("rate_limit_count")
		if !exists {
			counter = 0
		}

		if counter >= limiter.Limit {
			c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{"message": "Rate limit exceeded"})
			return
		}

		// Update counter and continue processing
		c.Set("rate_limit_count", counter+1)
		go func() {
			time.Sleep(limiter.Duration)
			c.Set("rate_limit_count", 0)
		}()

		c.Next()
	}
}
