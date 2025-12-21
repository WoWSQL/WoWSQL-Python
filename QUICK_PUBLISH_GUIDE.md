# 🚀 Quick Publish Guide - Python SDK

## ⚠️ CRITICAL: You MUST Build Before Uploading!

The error `Cannot find file (or expand pattern): 'dist/*'` means you need to **BUILD** the package first.

---

## 📋 Step-by-Step Instructions

### Step 1: Fix Version Mismatch (If Needed)

**Current Status:**
- ✅ `pyproject.toml`: `version = "1.2.0"`
- ✅ `src/wowsql/__init__.py`: `__version__ = "1.2.0"`

**Verify versions match:**
```powershell
cd sdk\python

# Check pyproject.toml version
Select-String -Path "pyproject.toml" -Pattern 'version\s*=\s*"([^"]+)"' | ForEach-Object { $_.Matches.Groups[1].Value }

# Check __init__.py version
Select-String -Path "src\wowsql\__init__.py" -Pattern '__version__\s*=\s*"([^"]+)"' | ForEach-Object { $_.Matches.Groups[1].Value }
```

**Both should show:** `1.2.0`

---

### Step 2: Install Build Tools

```powershell
pip install build twine
```

---

### Step 3: Clean Old Builds

```powershell
cd sdk\python

# Remove old build artifacts
Remove-Item -Recurse -Force dist,build -ErrorAction SilentlyContinue
Get-ChildItem -Filter "*.egg-info" -Recurse | Remove-Item -Recurse -Force
```

---

### Step 4: Build the Package ⭐ (REQUIRED!)

```powershell
cd sdk\python
python -m build
```

**Expected Output:**
```
* Creating venv isolated environment...
* Installing packages in isolated environment...
* Getting build dependencies...
* Building wheel...
* Building source distribution...
Successfully built wowsql-1.2.0-py3-none-any.whl
Successfully built wowsql-1.2.0.tar.gz
```

**Files Created:**
- `dist/wowsql-1.2.0-py3-none-any.whl`
- `dist/wowsql-1.2.0.tar.gz`

---

### Step 5: Verify Build

```powershell
python -m twine check dist/*
```

**Expected Output:**
```
Checking dist/wowsql-1.2.0-py3-none-any.whl: PASSED
Checking dist/wowsql-1.2.0.tar.gz: PASSED
```

---

### Step 6: Upload to PyPI

**Option A: Interactive (Easier)**
```powershell
python -m twine upload dist/*
```

When prompted:
- **Username:** `__token__` (with underscores)
- **Password:** Your PyPI API token (starts with `pypi-`)

**Option B: Using .pypirc file**

1. Create file: `C:\Users\YOUR_USERNAME\.pypirc`
2. Content:
   ```ini
   [pypi]
   username = __token__
   password = pypi-YOUR_TOKEN_HERE
   ```
3. Run:
   ```powershell
   python -m twine upload dist/*
   ```

---

## 🔍 Troubleshooting

### Error: "Cannot find file (or expand pattern): 'dist/*'"

**Cause:** You haven't built the package yet.

**Solution:**
```powershell
cd sdk\python
python -m build
```

### Error: "File already exists"

**Cause:** Version `1.2.0` already exists on PyPI.

**Solution:** Increment version in `pyproject.toml` and `__init__.py`, then rebuild.

### Error: "HTTPError: 403 Forbidden"

**Cause:** Invalid token or wrong username.

**Solution:**
- Username must be exactly: `__token__` (with underscores)
- Token must start with `pypi-`
- Make sure 2FA is enabled on PyPI account

---

## ✅ Success Checklist

After upload, verify:

- [ ] Package visible at: https://pypi.org/project/wowsql/
- [ ] Version `1.2.0` is listed
- [ ] Can install: `pip install wowsql`
- [ ] Can import: `from wowsql import WowSQLClient`

---

## 📝 Complete Command Sequence

```powershell
# 1. Navigate to SDK directory
cd sdk\python

# 2. Verify versions match
Select-String -Path "pyproject.toml" -Pattern 'version\s*=\s*"([^"]+)"'
Select-String -Path "src\wowsql\__init__.py" -Pattern '__version__\s*=\s*"([^"]+)"'

# 3. Install build tools (if needed)
pip install build twine

# 4. Clean old builds
Remove-Item -Recurse -Force dist,build -ErrorAction SilentlyContinue
Get-ChildItem -Filter "*.egg-info" -Recurse | Remove-Item -Recurse -Force

# 5. Build package
python -m build

# 6. Verify build
python -m twine check dist/*

# 7. Upload to PyPI
python -m twine upload dist/*
```

---

## 🎯 Current Status

- **Version:** `1.2.0`
- **Package Name:** `wowsql`
- **Build Status:** ⚠️ **NEEDS BUILD** (run `python -m build` first)
- **Upload Status:** ⏳ **PENDING** (build first)

---

**Remember:** Always run `python -m build` BEFORE `python -m twine upload`!

