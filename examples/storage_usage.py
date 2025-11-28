"""
WOWSQL Storage SDK - Python Examples
Demonstrates S3 storage operations with automatic quota validation
"""

from wowsql import WowSQLStorage, StorageLimitExceededError
import os

# Initialize storage client
storage = WowSQLStorage(
    project_slug="myproject",
    api_key="your_api_key_here",
    base_url="https://api.wowsql.com",
    auto_check_quota=True  # Automatically validate limits before upload
)


def example_1_check_quota():
    """Example 1: Check storage quota and usage"""
    print("\n=== Example 1: Check Storage Quota ===")
    
    quota = storage.get_quota()
    print(f"Plan: {quota.plan_name}")
    print(f"Total Storage: {quota.quota_gb + quota.expansion_gb:.2f} GB")
    print(f"Used: {quota.used_gb:.2f} GB ({quota.usage_percentage:.1f}%)")
    print(f"Available: {quota.available_gb:.2f} GB")
    
    if quota.can_expand:
        print("💡 You can expand storage (Enterprise plan)")


def example_2_upload_file():
    """Example 2: Upload a file with automatic limit validation"""
    print("\n=== Example 2: Upload File ===")
    
    try:
        # Upload from file path
        result = storage.upload_from_path(
            file_path='documents/report.pdf',
            folder='reports'
        )
        
        print(f"✓ Uploaded: {result['file_key']}")
        print(f"  Size: {result['file_size'] / (1024*1024):.2f} MB")
        print(f"  Bucket: {result['bucket_name']}")
        
    except StorageLimitExceededError as e:
        print(f"✗ Upload blocked: {e}")
        print("  → Consider upgrading your plan for more storage")
    except FileNotFoundError:
        print("✗ File not found")


def example_3_upload_from_bytes():
    """Example 3: Upload file from bytes/buffer"""
    print("\n=== Example 3: Upload from Bytes ===")
    
    try:
        # Read file content
        with open('images/photo.jpg', 'rb') as f:
            result = storage.upload_file(
                file_data=f,
                file_key='photo.jpg',
                folder='images',
                content_type='image/jpeg'
            )
        
        print(f"✓ Uploaded: {result['file_key']}")
        
    except StorageLimitExceededError as e:
        print(f"✗ Storage limit exceeded!")
        print(f"  Message: {e}")
        
        # Check how much space is available
        quota = storage.get_quota(force_refresh=True)
        print(f"  Available space: {quota.available_gb:.4f} GB")


def example_4_manual_quota_check():
    """Example 4: Manually check quota before upload"""
    print("\n=== Example 4: Manual Quota Check ===")
    
    file_size = 500 * 1024 * 1024  # 500 MB
    
    allowed, message = storage.check_upload_allowed(file_size)
    
    if allowed:
        print(f"✓ {message}")
        # Proceed with upload (disable auto-check since we already checked)
        # result = storage.upload_file(..., check_quota=False)
    else:
        print(f"✗ {message}")


def example_5_list_files():
    """Example 5: List files in storage"""
    print("\n=== Example 5: List Files ===")
    
    # List all files
    all_files = storage.list_files()
    print(f"Total files: {len(all_files)}")
    
    # List files in specific folder
    documents = storage.list_files(prefix='documents/')
    print(f"\nDocuments folder: {len(documents)} files")
    
    for file in documents[:5]:  # Show first 5
        print(f"  - {file.key}: {file.size_mb:.2f} MB")


def example_6_get_file_url():
    """Example 6: Get presigned URL for file access"""
    print("\n=== Example 6: Get File URL ===")
    
    file_key = 'documents/report.pdf'
    
    # Get presigned URL (valid for 1 hour)
    url_data = storage.get_file_url(file_key, expires_in=3600)
    
    print(f"File: {url_data['file_key']}")
    print(f"Download URL: {url_data['file_url'][:80]}...")
    print(f"Expires: {url_data['expires_at']}")
    print(f"Size: {url_data.get('size', 0) / (1024*1024):.2f} MB")


def example_7_delete_file():
    """Example 7: Delete a file"""
    print("\n=== Example 7: Delete File ===")
    
    result = storage.delete_file('old-files/temp.txt')
    print(f"✓ {result['message']}")
    
    # Quota is automatically refreshed after deletion
    quota = storage.get_quota()
    print(f"Available storage: {quota.available_gb:.2f} GB")


def example_8_storage_info():
    """Example 8: Get storage information"""
    print("\n=== Example 8: Storage Information ===")
    
    info = storage.get_storage_info()
    
    print(f"Bucket: {info['bucket_name']}")
    print(f"Region: {info['region']}")
    print(f"Status: {info['status']}")
    print(f"Total Objects: {info['total_objects']}")
    print(f"Total Size: {info['total_size_gb']:.2f} GB")


def example_9_provision_storage():
    """Example 9: Provision S3 storage (first time setup)"""
    print("\n=== Example 9: Provision Storage ===")
    
    try:
        # Get available regions first
        regions = storage.get_available_regions()
        print("Available regions:")
        for region in regions[:3]:  # Show first 3
            print(f"  - {region['name']}: ${region['storage_price_gb']}/GB/month")
        
        # Provision storage
        result = storage.provision_storage(region='us-east-1')
        
        print(f"\n✓ Storage provisioned successfully!")
        print(f"  Bucket: {result['bucket_name']}")
        print(f"  Region: {result['region']}")
        print(f"\n⚠️  IMPORTANT: Save these credentials (shown only once):")
        print(f"  Access Key: {result['credentials']['access_key_id']}")
        print(f"  Secret Key: {result['credentials']['secret_access_key']}")
        
    except Exception as e:
        print(f"Note: Storage may already be provisioned")


def example_10_error_handling():
    """Example 10: Comprehensive error handling"""
    print("\n=== Example 10: Error Handling ===")
    
    try:
        # Try to upload a large file
        large_file_data = b"x" * (1024 ** 3 * 2)  # 2 GB
        
        result = storage.upload_file(
            file_data=large_file_data,
            file_key='large-file.bin'
        )
        
    except StorageLimitExceededError as e:
        print(f"✗ Storage Limit Exceeded:")
        print(f"  Status Code: {e.status_code}")
        print(f"  Message: {e}")
        
        # Get current quota to show user
        quota = storage.get_quota(force_refresh=True)
        print(f"\n📊 Current Usage:")
        print(f"  Plan: {quota.plan_name}")
        print(f"  Used: {quota.used_gb:.2f} GB / {quota.quota_gb + quota.expansion_gb:.2f} GB")
        print(f"  Available: {quota.available_gb:.2f} GB")
        
        if not quota.is_enterprise:
            print(f"\n💡 Tip: Upgrade to a higher plan for more storage!")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def example_11_context_manager():
    """Example 11: Using context manager (auto-close session)"""
    print("\n=== Example 11: Context Manager ===")
    
    with WowSQLStorage(
        project_slug="myproject",
        api_key="your_api_key_here"
    ) as storage_client:
        quota = storage_client.get_quota()
        print(f"Available: {quota.available_gb:.2f} GB")
        
        # Upload files...
        # Session automatically closed when exiting context


def example_12_batch_upload():
    """Example 12: Batch upload with progress tracking"""
    print("\n=== Example 12: Batch Upload ===")
    
    files_to_upload = [
        ('file1.txt', 'folder1'),
        ('file2.txt', 'folder1'),
        ('image.jpg', 'images'),
    ]
    
    # Check total size first
    total_size = sum(os.path.getsize(f[0]) for f in files_to_upload if os.path.exists(f[0]))
    allowed, message = storage.check_upload_allowed(total_size)
    
    if not allowed:
        print(f"✗ Cannot upload batch: {message}")
        return
    
    print(f"✓ Starting batch upload ({total_size / (1024*1024):.2f} MB)...")
    
    for file_path, folder in files_to_upload:
        try:
            if os.path.exists(file_path):
                result = storage.upload_from_path(
                    file_path=file_path,
                    folder=folder,
                    check_quota=False  # Already checked total
                )
                print(f"  ✓ {result['file_key']}")
        except Exception as e:
            print(f"  ✗ {file_path}: {e}")
    
    print("Batch upload complete!")


# Run examples
if __name__ == "__main__":
    print("=" * 60)
    print("WOWSQL Storage SDK - Python Examples")
    print("=" * 60)
    
    # Note: Make sure to set your actual project slug and API key above
    
    # Run individual examples
    try:
        example_1_check_quota()
        # example_2_upload_file()
        # example_3_upload_from_bytes()
        # example_4_manual_quota_check()
        # example_5_list_files()
        # example_6_get_file_url()
        # example_7_delete_file()
        # example_8_storage_info()
        # example_9_provision_storage()
        # example_10_error_handling()
        # example_11_context_manager()
        # example_12_batch_upload()
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure to:")
        print("1. Set your actual project_slug and api_key")
        print("2. Provision storage for your project first")
        print("3. Have files ready to upload (or adjust file paths)")

