# Production checklist

- [ ] Replace SECRET_KEY and JWT_SECRET_KEY with long random values.
- [ ] Use PostgreSQL in production.
- [ ] Restrict CORS_ORIGINS to the deployed frontend domain.
- [ ] Put uploads in private object storage if farmer data must be protected.
- [ ] Add rate limiting before public launch.
- [ ] Add virus/content scanning if arbitrary uploads are allowed.
- [ ] Configure HTTPS.
- [ ] Add database backups.
- [ ] Add logs and monitoring.
- [ ] Add model version to every Scan record.
- [ ] Validate model confidence and out-of-distribution images.
- [ ] Use trusted agricultural sources for recommendations.
- [ ] Never generate unsupported pesticide dosage instructions.
- [ ] Add consent/privacy notice for location and uploaded images.
