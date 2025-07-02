# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in OGPW, please report it responsibly:

1. **Do not** open a public issue
2. Email security concerns to: security@ogpw.dev
3. Include detailed steps to reproduce
4. Allow time for investigation and patching

## Security Considerations

### File Upload Security
- Only .pcap and .pcapng files are accepted
- File size limited to 500MB
- Files are processed locally and not stored permanently
- Input validation on all uploaded content

### API Security
- CORS properly configured
- Input validation on all endpoints
- Error handling prevents information disclosure
- Rate limiting recommended for production

### Data Privacy
- PCAP files are analyzed locally
- No data is transmitted to external services (except OpenAI if configured)
- Temporary files are cleaned up after processing

### Production Deployment
- Change default secret keys
- Use HTTPS in production
- Implement proper authentication if needed
- Regular security updates
- Monitor for suspicious activity

## Best Practices

1. Keep dependencies updated
2. Use environment variables for sensitive data
3. Enable logging and monitoring
4. Regular security audits
5. Backup important data