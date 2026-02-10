# ✅ Installation Verification Guide

This document helps you verify that FlashMaster is installed correctly and all features are working.

## Pre-Installation Checklist

- [ ] Python 3.8 or higher installed
- [ ] pip installed
- [ ] Git installed (optional)
- [ ] Text editor or IDE ready

## Installation Steps Verification

### Step 1: Project Files
```bash
cd flashcard_app
ls -la
```

**Expected Output:**
- manage.py
- requirements.txt
- README.md
- setup.sh / setup.bat
- accounts/ directory
- flashcards/ directory
- flashcard_project/ directory
- templates/ directory

✅ **Pass**: All files and directories are present

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected Output:**
- Successfully installed Django-4.x.x

✅ **Pass**: Django installed without errors

### Step 3: Database Setup
```bash
python manage.py makemigrations accounts
python manage.py makemigrations flashcards
python manage.py migrate
```

**Expected Output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying accounts... OK
  Applying flashcards... OK
  ...
```

✅ **Pass**: Migrations applied successfully

### Step 4: Create Superuser
```bash
python manage.py createsuperuser
```

**Expected Output:**
- Prompts for username, email, password
- User created successfully

✅ **Pass**: Superuser created

### Step 5: Start Server
```bash
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

✅ **Pass**: Server running without errors

## Feature Testing Checklist

### 1. Authentication Features

#### Test Signup
1. Navigate to: http://127.0.0.1:8000/accounts/signup/
2. Fill in registration form
3. Submit form

✅ **Expected**: 
- Redirected to dashboard
- Welcome message appears
- User is logged in

#### Test Login
1. Logout if logged in
2. Navigate to: http://127.0.0.1:8000/accounts/login/
3. Enter credentials
4. Submit form

✅ **Expected**:
- Redirected to dashboard
- Success message appears
- User is logged in

#### Test Profile
1. Click on username dropdown
2. Click "Profile"

✅ **Expected**:
- Profile page loads
- Shows user information
- Shows statistics

### 2. Flashcard Features

#### Test Create Flashcard
1. Click "Create Card" in navigation
2. Fill in:
   - Topic: "Test"
   - Question: "What is 2+2?"
   - Answer: "4"
3. Submit form

✅ **Expected**:
- Flashcard created
- Success message
- Redirected to list

#### Test View Flashcards
1. Click "My Cards" in navigation

✅ **Expected**:
- List of flashcards displayed
- Search and filter options visible
- Cards show topic, question preview

#### Test Edit Flashcard
1. Click edit icon on a flashcard
2. Modify content
3. Save changes

✅ **Expected**:
- Changes saved
- Success message
- Updated content visible

#### Test Delete Flashcard
1. Click delete icon on a flashcard
2. Confirm deletion

✅ **Expected**:
- Confirmation page appears
- After confirm, flashcard deleted
- Success message

### 3. Study Mode Features

#### Test Study Mode
1. Click "Study Mode" in navigation
2. Click on flashcard to flip
3. Click "I Know This" button

✅ **Expected**:
- Card flips with animation
- Progress bar updates
- Next card appears

#### Test Keyboard Shortcuts
1. In study mode
2. Press Space/Enter to flip
3. Press → or K to mark known
4. Press ← or R to review later

✅ **Expected**:
- Card flips on Space/Enter
- Card marked and moves to next on arrows

#### Test Filters
1. In study mode
2. Use topic filter dropdown
3. Try "Review Only" filter

✅ **Expected**:
- Cards filtered correctly
- Only matching cards shown

### 4. Statistics Features

#### Test Dashboard
1. Navigate to dashboard

✅ **Expected**:
- Total cards displayed
- Known/Review counts shown
- Topics listed
- Recent sessions visible

#### Test Statistics Page
1. Click "Statistics" in navigation

✅ **Expected**:
- Detailed statistics shown
- Topic breakdown with progress bars
- Study session history
- Success rates displayed

### 5. Import/Export Features

#### Test Export
1. Click user menu → More → Export CSV
2. Download file

✅ **Expected**:
- CSV file downloads
- Contains all flashcards
- Proper formatting

#### Test Import
1. Click "Import" or navigate to import page
2. Select sample_flashcards.csv
3. Submit

✅ **Expected**:
- Success message
- Flashcards imported
- Visible in card list

### 6. Theme Features

#### Test Theme Toggle
1. Click moon/sun icon in navbar
2. Toggle between light and dark

✅ **Expected**:
- Theme changes smoothly
- All elements update
- Preference persists on reload

### 7. Admin Panel

#### Test Admin Access
1. Navigate to: http://127.0.0.1:8000/admin/
2. Login with superuser credentials

✅ **Expected**:
- Admin panel loads
- Can see Users, Flashcards, Study Sessions
- Can add/edit/delete items

## Common Issues & Solutions

### Issue: "Django not found"
**Solution:**
```bash
pip install django
```

### Issue: "Table doesn't exist"
**Solution:**
```bash
python manage.py migrate
```

### Issue: "Port already in use"
**Solution:**
```bash
python manage.py runserver 8080
```

### Issue: "Static files not loading"
**Solution:**
```bash
python manage.py collectstatic
```

### Issue: "Permission denied on manage.py"
**Solution:**
```bash
chmod +x manage.py
```

## Performance Verification

### Load Time Test
1. Open browser developer tools
2. Navigate to dashboard
3. Check Network tab

✅ **Expected**:
- Page loads in < 2 seconds
- No 404 errors
- All resources load

### Responsiveness Test
1. Open browser developer tools
2. Toggle device toolbar
3. Test different screen sizes:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1920px)

✅ **Expected**:
- Layout adapts to screen size
- All features accessible
- No horizontal scrolling

## Security Verification

### CSRF Protection
1. Inspect any form
2. Look for hidden input with name="csrfmiddlewaretoken"

✅ **Expected**: CSRF token present

### Authentication Protection
1. Logout
2. Try to access: http://127.0.0.1:8000/flashcards/create/

✅ **Expected**: Redirected to login page

### User Data Isolation
1. Create flashcards with User A
2. Logout and login as User B
3. Check flashcard list

✅ **Expected**: User B cannot see User A's flashcards

## Final Verification

Run all tests:
```bash
python manage.py test
```

✅ **Expected**: All tests pass

## Installation Complete! ✅

If all checks pass:
- ✅ Installation successful
- ✅ All features working
- ✅ Security measures active
- ✅ Ready for use

## Next Steps

1. Create your first flashcard
2. Start studying
3. Track your progress
4. Export your data for backup
5. Explore advanced features

## Support

If any test fails:
1. Check the error message
2. Refer to README.md
3. Check QUICKSTART.md
4. Review common issues above
5. Check Django documentation

---

**Congratulations! FlashMaster is ready to use! 🎉**
