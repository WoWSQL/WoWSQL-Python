# Changelog

All notable changes to the WOWSQL Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-11-22

### Added - Schema Management 🔧

- **New `WOWSQLSchema` class** for programmatic database schema management
- Full schema CRUD operations with service role key authentication
- Schema modification capabilities for production databases

#### Schema Features
- **Create Tables**: Define tables with columns, primary keys, and indexes
- **Alter Tables**: Add, modify, drop, or rename columns
- **Drop Tables**: Remove tables with optional CASCADE support
- **Execute SQL**: Run raw SQL for custom schema operations

#### Schema API Methods
- `create_table()` - Create new tables with full column definitions
- `alter_table()` - Modify existing table structure
- `drop_table()` - Drop tables safely
- `execute_sql()` - Execute custom schema SQL statements

#### Security & Validation
- **Service Role Key Required**: Schema operations strictly require service role keys
- **403 Error Handling**: Clear error messages when using anonymous keys
- **Permission Validation**: Automatic validation of API key permissions
- `PermissionError` exception for schema permission errors

#### Examples & Documentation
- Backend migration script examples
- Schema management best practices
- Security guidelines for service key usage
- Comprehensive README section with code examples

### Updated
- README with comprehensive schema management documentation
- `__init__.py` exports to include `WOWSQLSchema` and `PermissionError`
- Version bumped to 0.5.0

### Documentation
- Schema management quick start guide
- Service role key vs anonymous key usage
- Migration script templates
- Error handling patterns

## [0.3.0] - 2025-11-10

### Added - Project Authentication

- **New `ProjectAuthClient`** for signup/login/OAuth flows

### Added - S3 Storage Support 🚀

#### Storage Client
- **New `WOWSQLStorage` class** for S3-compatible object storage
- Full CRUD operations for file management
- Storage quota tracking and enforcement
- Client-side storage limit validation
- Multi-region support
- Context manager support for automatic cleanup

#### Storage Features
- **File Upload**: Upload files with automatic quota checking
- **File Download**: Get presigned URLs or download files directly
- **File Listing**: List all files with metadata (size, type, modified date)
- **File Deletion**: Delete files and free up storage space
- **Quota Management**: Check available storage and usage limits
- **Batch Operations**: Delete multiple files at once

#### Storage API Methods
- `upload(file_path, key, metadata=None)` - Upload file to S3
- `upload_fileobj(file_obj, key, metadata=None)` - Upload file-like object
- `download(key, destination=None)` - Download file or get presigned URL
- `list_files(prefix=None, limit=None)` - List files with optional filtering
- `delete_file(key)` - Delete single file from storage
- `delete_files(keys)` - Delete multiple files at once
- `get_quota()` - Get storage quota information
- `get_file_info(key)` - Get detailed file metadata
- `file_exists(key)` - Check if file exists
- `get_file_size(key)` - Get file size in bytes

#### Storage Error Handling
- `StorageLimitExceededError` - Raised when storage quota is exceeded
- `StorageError` - Base exception class for storage operations
- Comprehensive error messages with suggestions
- Automatic cleanup on upload failures

#### Storage Types
- `StorageQuota` - Storage limit and usage information (dataclass)
- `StorageFile` - File metadata (dataclass)
- Complete type hints throughout

#### Examples
- Complete storage usage examples in `examples/storage_usage.py`
- File upload/download workflows
- Quota management patterns
- Error handling best practices
- Batch operations examples

### Updated
- Package description to mention S3 Storage support
- Version bumped to 0.2.0
- Export statements in `__init__.py` to include storage classes
- Documentation URL updated to `https://wowsql.com/docs`

### Documentation
- Storage SDK architecture diagram
- Quick start guide for storage
- API reference for storage methods
- Implementation examples

### Requirements
- No new dependencies added (uses existing `requests` library)
- Compatible with Python 3.8+

## [0.1.3] - 2025-10-10

### Added
- Complete Python SDK with type hints
- Fluent query builder API
- Support for all CRUD operations (Create, Read, Update, Delete)
- Advanced filtering with multiple operators (eq, neq, gt, gte, lt, lte, like, is_null)
- Pagination support (limit, offset)
- Sorting capabilities (order_by)
- Raw SQL query execution
- Table schema introspection
- Health check endpoint
- Comprehensive error handling with `WOWSQLError` class
- Type-safe queries with Python type hints
- Context manager support
- Configurable timeout option

### Features
- **Simple API**: Easy-to-use Pythonic interface
- **Type-Safe**: Full type hints for better IDE support
- **Fluent API**: Chainable query builder pattern
- **Lightweight**: Minimal dependencies (only requests)
- **Error Handling**: Comprehensive error messages

### Examples
- Basic CRUD operations
- Complex queries with filtering
- Context manager usage
- Error handling patterns

### Documentation
- Complete README with usage examples
- API reference
- Best practices guide
- Publishing guide for PyPI

## [0.1.0] - Initial Release

### Added
- Basic REST API client
- Simple query methods
- Authentication with API keys
- Table operations

---

## Upgrade Guide

### From 0.1.x to 0.2.0

The 0.2.0 release adds S3 storage support with no breaking changes to existing database functionality.

#### New Features

1. **Import storage classes**
   ```python
   from WOWSQL import WOWSQLStorage, StorageQuota, StorageFile
   ```

2. **Initialize storage client**
   ```python
   storage = WOWSQLStorage(
       project_url="https://myproject.wowsql.com",
       api_key="your-api-key"
   )
   ```

3. **Use storage operations**
   ```python
   # Upload file
   storage.upload("local-file.pdf", "uploads/file.pdf")
   
   # Get quota
   quota = storage.get_quota()
   print(f"Used: {quota.used_bytes} / {quota.limit_bytes}")
   
   # List files
   files = storage.list_files(prefix="uploads/")
   
   # Download file
   url = storage.download("uploads/file.pdf")
   ```

#### Migration Steps

1. Update package:
   ```bash
   pip install --upgrade wowsql
   ```

2. No changes needed to existing database code

3. Add storage operations where needed

4. Handle new `StorageLimitExceededError` exception

5. Test storage operations in development

---

## Future Roadmap

### Planned Features

- [ ] Async/await support (`AsyncWOWSQLClient`)
- [ ] Connection pooling for better performance
- [ ] Transaction support
- [ ] Batch operations for database queries
- [ ] Query caching
- [ ] Retry logic with exponential backoff
- [ ] Streaming uploads for large files
- [ ] Storage events/webhooks
- [ ] File versioning support
- [ ] Aggregation functions (COUNT, SUM, AVG, etc.)

### Under Consideration

- [ ] Django ORM integration
- [ ] SQLAlchemy adapter
- [ ] CLI tool for migrations
- [ ] Query performance monitoring
- [ ] Local storage emulator for testing
- [ ] Compression support for uploads

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.

## Support

- 📧 Email: support@wowsql.com
- 💬 Discord: [Join our community](https://discord.gg/WOWSQL)
- 📚 Documentation: [https://wowsql.com/docs](https://wowsql.com/docs)
- 🐛 Issues: [GitHub Issues](https://github.com/wowsql/wowsql/issues)

---

For more information, visit [https://wowsql.com](https://wowsql.com)

