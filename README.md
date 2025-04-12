# Setup
## 1. Python Webpack Boilerplate
````shell
python manage.py webpack_init
````
## 2. Download Node.js
### Download and install nvm:
````shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
````
### in lieu of restarting the shell
````shell
\. "$HOME/.nvm/nvm.sh"
````
### Download and install Node.js:
````shell
nvm install 22
````
### Verify the Node.js version:
````shell
node -v # Should print "v22.14.0".
nvm current # Should print "v22.14.0".
````
### Verify npm version:
````shell
npm -v # Should print "10.9.2".
# install dependency packages
npm install
# run webpack in watch mode
npm run watch
````
