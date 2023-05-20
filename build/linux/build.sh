echo "Creating Poricom pyinstaller package"
pyinstaller main.spec

echo "Bundle Poricom for distribution"
mkdir -p package/opt
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/scalable/apps

cp -r dist/app package/opt/poricom
cp poricom.desktop package/usr/share/applications
cp package/opt/poricom/assets/images/icons/logo.svg package/usr/share/icons/hicolor/scalable/apps/logo.svg

find package/opt/poricom -type f -exec chmod 644 -- {} +
find package/opt/poricom -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +
chmod +x package/opt/poricom/Poricom

echo "Create deb package"
#sudo apt install ruby -y
#gem install fpm
fpm -C package -s dir -t deb -n "poricom" -v 1.0.0 -p poricom.deb

echo "Linux build (deb) finished."
