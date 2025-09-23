# Git Push Guide

## Step 1: Initialize Git (if not already done)
```bash
git init
```

## Step 2: Add your GitHub repository as remote
```bash
git remote add origin https://github.com/YOUR_USERNAME/qr-attendance-system.git
```
*Replace YOUR_USERNAME with your actual GitHub username*

## Step 3: Add all files to staging
```bash
git add .
```

## Step 4: Commit the changes
```bash
git commit -m "Clean up project structure and add setup scripts

- Removed duplicate and unnecessary files
- Added setup.py for automated database initialization
- Added run.py for easier application startup
- Updated README with improved documentation
- Added proper .gitignore for Python projects
- Organized project structure for better maintainability"
```

## Step 5: Push to GitHub
```bash
git push -u origin main
```

## Alternative: If you have an existing repository
```bash
git add .
git commit -m "Project cleanup and improvements"
git push origin main
```

## If you encounter authentication issues:
1. Use GitHub CLI: `gh auth login`
2. Or use personal access token instead of password
3. Or use SSH key authentication

## Files that will be pushed:
- ✅ Cleaned project structure
- ✅ All original functionality preserved
- ✅ New setup and run scripts
- ✅ Updated documentation
- ✅ Proper .gitignore file