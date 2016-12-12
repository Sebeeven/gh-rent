## 简易的命令行入门教程:

### Git 全局设置:
```bash  
git config --global user.name "xxx"
git config --global user.email "xxx"
```  
### 创建 git 仓库:
```bash  
mkdir RentWebsite
cd RentWebsite
git init
touch README.md
git add README.md
git commit -m "first commit"
git remote add origin https://git.oschina.net/sebeeven/RentWebsite.git
git push -u origin master
```

### 已有项目?
```bash
cd existing_git_repo
git remote add origin https://git.oschina.net/sebeeven/RentWebsite.git
git push -u origin master
```