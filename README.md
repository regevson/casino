<div align="center"><img width="30%" src="img/logo.png"></div>

# 🎰 **Casino Blocker**

**Casino Blocker** is a tool designed to help individuals avoid online gambling sites, especially beneficial for those seeking to overcome gambling addictions. It uses a **bag of words model** and a **random forest classifier** to identify and block casino websites.

## 📝 **Overview**

The project was initiated to block gambling sites not usually covered by standard blocklists, with a focus on multi-lingual sites, and to address the issue of frequently changing URLs. **Casino Blocker** operates by allowing only pre-approved websites, with a feature for dynamically analyzing and blocking harmful sites.

**A novel, publicly accessible [dataset](research/data)**, comprising **1,000 instances** of website text, was created for this project, with each instance **manually labeled as belonging to one of two categories**: 'gambling site' or 'regular site'. This dataset was sourced from **blocklists** and **government-blocked** casino lists.

## 🛠 **How to Use**

1. **Parental Controls**: On iOS, enable parental controls to block all websites except certain specified ones.
2. **Permitted URL**: Add 'casino.regevson.com' as a permitted URL.
3. **Lock Settings**: Have a friend lock these settings with a code unknown to you.
4. **Website Analysis**: Paste URLs into the search bar on [casino.regevson.com](https://casino.regevson.com). Websites are downloaded to the server for display and background analysis.
5. **Blocking**: If a site is classified as harmful, it's blocked.

## 🚀 **How to Run**

1. Clone the repository.
2. Install required Python packages.
3. Run `uvicorn casino:app --reload`.

## 🔍 **Technical Details**

- **Classifier**: We experimented with SVM, logistic regression, and random forest classifiers using a bag of words model. The **random forest classifier** emerged as the most effective, offering an **accuracy** of **95%**.
- **Backend**: Implemented with **FastAPI** for easy server-side development.
- **Frontend**: Developed using standard HTML/CSS/JS.
- **Website Download**: Utilizes **wget** for downloading website content.

## ⚠️ **Limitations**

- **JavaScript Support**: The system does not support JavaScript, affecting the functionality of some sites.
- **Speed**: The process is slower than regular browsing due to the need to download websites for analysis.
- **Manual Enabling**: Sites relying heavily on JavaScript may require manual enabling in the settings.

## 🔮 **Future Work**

- Enhance the classifier with advanced NLP techniques.
- Explore solutions for JavaScript compatibility.
- Improve processing speed for a more seamless browsing experience.

## ❓ **FAQs/Troubleshooting**

- **Q: What to do if a legitimate website is blocked?**
  - **A:** Manually add the website to the allowed list in your parental control settings.

- **Q: What should I do if the website is not loading properly?**
  - **A:** The website most likely relies on JavaScript and at the moment this poses a problem. Please manually add the website to the allowed list in your parental control settings.
