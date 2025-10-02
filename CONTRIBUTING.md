# **Contributing to Web Crawler**  

Thanks for wanting to help make this thing better! Here's how you can contribute without making a mess.  

## **How to Contribute**  

### **Found a Bug?**  
1. Check if someone already reported it in the [Issues](https://github.com/ThutaCodes/webspider/issues).  
2. If not, **open a new issue** with:  
   - What you expected to happen  
   - What actually happened  
   - Steps to reproduce it  
   - Your Python version and OS  

### **Have an Idea?**  
1. Open an issue first to discuss it.  
2. Wait for feedback before starting to code.  
3. Nobody wants to reject a PR after you spent hours on it.  

## **Making Changes**  

### **1. Fork & Clone**  
```bash
git clone https://github.com/YOUR_USERNAME/webspider
cd webspider
```  

### **2. Create a Branch**  
```bash
git checkout -b fix-something-cool
```  

### **3. Set Up Your Environment**  
Follow the setup instructions in the [README.md](README.md).  

### **4. Make Your Changes**  
- Keep it simple and focused.  
- One feature or fix per PR.  
- Don't rewrite the entire project.  

### **5. Test Your Changes**  
```bash
python3 spider.py
```  
Make sure it still works and doesn't break anything.  

### **6. Commit & Push**  
```bash
git add .
git commit -m "Fix: describe what you fixed"
git push origin fix-something-cool
```  

### **7. Open a Pull Request**  
- Describe what you changed and why.  
- Reference any related issues.  
- Be patient while waiting for a review.  

## **Code Style**  

- Follow **PEP 8** for Python code.  
- Use meaningful variable names.  
- Add comments when something isn't obvious.  
- Don't over-complicate things.  

## **What Gets Accepted**  

✅ **Good stuff:**  
- Bug fixes  
- Performance improvements  
- New features that make sense  
- Better error handling  
- Documentation improvements  

❌ **Not so good:**  
- Breaking changes without discussion  
- Unnecessary dependencies  
- Code that only works on your machine  
- Huge refactors without prior approval  

## **Questions?**  

Open an issue or reach out. We don't bite.  

---

**Thanks for contributing!** 🎉  
