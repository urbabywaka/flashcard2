# 🔧 Study Mode Button Fix Guide

## Problem: "I Know This" and "Review Later" buttons not working

This guide will help you fix and test the study mode buttons.

## ✅ Quick Fix Steps

### Step 1: Stop the Server
In your VS Code terminal, press **Ctrl + C** to stop the Django server.

### Step 2: Download the Updated Files
Download the new **flashcard_app.zip** or **flashcard_app.tar.gz** and replace the old files.

### Step 3: Restart the Server
```bash
python manage.py runserver
```

### Step 4: Hard Refresh Browser
- Press **Ctrl + Shift + R** (Windows/Linux)
- Or **Cmd + Shift + R** (Mac)

This clears the browser cache and loads the new JavaScript.

---

## 🧪 Testing the Buttons

1. **Open Study Mode**: http://127.0.0.1:8000/flashcards/study/
2. **Open Browser Console** (Press F12)
3. **Click "I Know This"**

### ✅ What You Should See:

**In Browser Console:**
```
Marking card: 1 as known
Response status: 200
Response data: {status: 'success', message: 'Card marked as known!', is_known: true}
```

**On Screen:**
- Progress bar updates
- "Known: 1" counter increases
- Next card appears

### ❌ If You See Errors:

#### Error: "403 Forbidden"
**Cause:** CSRF token issue

**Fix:**
1. Open browser developer tools (F12)
2. Go to **Application** tab
3. Click **Cookies** → http://127.0.0.1:8000
4. Check if `csrftoken` cookie exists

If missing, **hard refresh** the page (Ctrl + Shift + R)

#### Error: "404 Not Found"
**Cause:** URL routing issue

**Fix:** Check that you're accessing the correct URL:
- Should be: `http://127.0.0.1:8000/flashcards/study/`
- Not: `http://127.0.0.1:8000/study/`

#### Error: "Network Error"
**Cause:** Server not running

**Fix:**
```bash
python manage.py runserver
```

---

## 🔍 Manual Testing Checklist

### Test 1: Check JavaScript is Loaded
1. Open study mode
2. Press F12 (Developer Tools)
3. Go to **Console** tab
4. Type: `cards`
5. Press Enter

**Expected:** Should show array of flashcard objects
```javascript
[{id: 1, topic: "Math", front: "...", back: "..."}, ...]
```

### Test 2: Check CSRF Token Function
1. In console, type: `getCookie('csrftoken')`
2. Press Enter

**Expected:** Should show a long string (the CSRF token)
```
"abc123def456..."
```

### Test 3: Check Mark Function Exists
1. In console, type: `typeof markCard`
2. Press Enter

**Expected:** `"function"`

### Test 4: Manually Call Function
1. In console, type: `markCard('known')`
2. Press Enter

**Expected:** 
- Card should advance to next
- Console shows success logs

---

## 🛠️ Alternative Fix: Manual File Update

If downloading new files doesn't work, manually update these files:

### File 1: `templates/flashcards/study_mode.html`

Find this section (around line 260):
```javascript
function markCard(action) {
    const card = cards[currentIndex];
    
    // OLD CODE - Remove console.log if it doesn't exist
```

Replace with:
```javascript
function markCard(action) {
    const card = cards[currentIndex];
    
    console.log('Marking card:', card.id, 'as', action);
    
    fetch(`/flashcards/${card.id}/mark/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `action=${action}`
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.status === 'success') {
            if (action === 'known') {
                knownCount++;
                document.getElementById('known-count').textContent = `Known: ${knownCount}`;
            }
            currentIndex++;
            loadCard();
        } else {
            console.error('Error:', data.message);
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        alert('Network error. Please try again.');
    });
}
```

---

## 📊 Success Indicators

When working correctly, you should see:

1. **Progress bar** moves forward
2. **"Known: X"** counter increases (for "I Know This")
3. **Card smoothly transitions** to next card
4. **No errors** in console
5. **After all cards**: Completion modal appears

---

## 🎯 Still Not Working?

### Check Server Logs

In your terminal (where server is running), you should see:
```
[05/Feb/2026 15:30:45] "POST /flashcards/1/mark/ HTTP/1.1" 200 60
```

**200** = Success ✅
**403** = CSRF error ❌
**404** = URL not found ❌
**500** = Server error ❌

### Check Database

Verify flashcards exist:
```bash
python manage.py shell
```

Then in the shell:
```python
from flashcards.models import Flashcard
from django.contrib.auth.models import User

user = User.objects.first()
cards = Flashcard.objects.filter(user=user)
print(f"You have {cards.count()} flashcards")
```

Expected: Should show number > 0

---

## 💡 Quick Debug Mode

Add this to the top of your `markCard` function for detailed debugging:

```javascript
function markCard(action) {
    console.log('=== DEBUG START ===');
    console.log('Current index:', currentIndex);
    console.log('Total cards:', cards.length);
    console.log('Card:', cards[currentIndex]);
    console.log('Action:', action);
    console.log('CSRF Token:', getCookie('csrftoken'));
    console.log('=== DEBUG END ===');
    
    // ... rest of function
}
```

This will show you exactly what's happening when you click the buttons!

---

## ✅ Final Verification

Everything working when you see:
1. ✅ Console logs appear when clicking buttons
2. ✅ Card advances to next
3. ✅ Progress bar updates
4. ✅ Counter increases
5. ✅ No red errors in console

**Good luck! The buttons should work now! 🎉**
