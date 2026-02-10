# 📋 Render Deployment Checklist

Use this checklist to ensure you don't miss any steps!

## ✅ Pre-Deployment (Local Setup)

- [ ] Install production dependencies: `pip install -r requirements.txt`
- [ ] Test locally with updated settings
- [ ] Files exist:
  - [ ] `build.sh`
  - [ ] `runtime.txt`
  - [ ] `requirements.txt` (updated)
  - [ ] `.gitignore`
- [ ] `build.sh` is executable: `chmod +x build.sh`

## ✅ GitHub Setup

- [ ] Created GitHub repository
- [ ] Initialized git: `git init`
- [ ] Added files: `git add .`
- [ ] Committed: `git commit -m "Initial commit"`
- [ ] Added remote: `git remote add origin <YOUR_REPO_URL>`
- [ ] Pushed: `git push -u origin main`

## ✅ Render Account Setup

- [ ] Created Render account at https://render.com
- [ ] Connected GitHub account
- [ ] Verified email (if required)

## ✅ Database Setup

- [ ] Created PostgreSQL database
  - [ ] Name: `flashcard-db`
  - [ ] Plan: Free
- [ ] Copied **Internal Database URL**
- [ ] Saved URL securely

## ✅ Web Service Setup

- [ ] Created Web Service
- [ ] Connected to GitHub repository
- [ ] Configured settings:
  - [ ] Name: `flashcard-app` (or your choice)
  - [ ] Branch: `main`
  - [ ] Build Command: `./build.sh`
  - [ ] Start Command: `gunicorn flashcard_project.wsgi:application`
  - [ ] Plan: Free

## ✅ Environment Variables

Added all environment variables:

- [ ] `PYTHON_VERSION` = `3.11.0`
- [ ] `SECRET_KEY` = (generated random key)
- [ ] `DEBUG` = `False`
- [ ] `DATABASE_URL` = (Internal Database URL)

**Generate SECRET_KEY with:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## ✅ Deployment

- [ ] Clicked "Create Web Service"
- [ ] Waited for build to complete (5-10 min)
- [ ] Build succeeded ✅
- [ ] Service is live ✅

## ✅ Post-Deployment

- [ ] Accessed app URL: `https://your-app.onrender.com`
- [ ] Created superuser:
  - [ ] Opened Shell in Render dashboard
  - [ ] Ran: `python manage.py createsuperuser`
  - [ ] Created admin account

## ✅ Testing

Test all features on live site:

- [ ] Homepage loads correctly
- [ ] Sign up works
- [ ] Login works
- [ ] Create flashcard works
- [ ] View flashcards works
- [ ] Edit flashcard works
- [ ] Delete flashcard works
- [ ] Study mode works
- [ ] "I Know This" button works
- [ ] "Review Later" button works
- [ ] Card flip animation works
- [ ] Progress tracking works
- [ ] Dark mode toggle works
- [ ] Statistics page works
- [ ] Import CSV works
- [ ] Export CSV works
- [ ] Admin panel works: `/admin`

## ✅ Optional Enhancements

- [ ] Added custom domain
- [ ] Set up monitoring
- [ ] Configured backup strategy
- [ ] Added error tracking (e.g., Sentry)

## 🎉 Success Criteria

Your deployment is successful when:

✅ App URL works and loads properly
✅ All features tested and working
✅ Database connected and persistent
✅ Static files (CSS) loading correctly
✅ No errors in Render logs
✅ Admin panel accessible
✅ Can create and manage flashcards

---

## 🆘 If Something Fails

### Build Failed
1. Check Render build logs
2. Verify `requirements.txt` is correct
3. Check `build.sh` is executable
4. Make sure all files are pushed to GitHub

### Database Connection Failed
1. Verify `DATABASE_URL` is correct
2. Use **Internal** URL, not External
3. Check PostgreSQL service is running

### Static Files Not Loading
1. Verify WhiteNoise in middleware
2. Check `STATICFILES_STORAGE` setting
3. Run `python manage.py collectstatic` in Shell

### 500 Error
1. Check Render logs for error details
2. Verify all environment variables are set
3. Check `DEBUG = False` in production
4. Ensure migrations ran: `python manage.py migrate`

---

## 📝 Quick Commands (Render Shell)

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Check setup
python manage.py check

# Open Django shell
python manage.py shell
```

---

**Print this checklist and check off each item as you complete it!** ✓
