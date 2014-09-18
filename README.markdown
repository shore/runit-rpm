# What the?

I like [runit](http://smarden.org/runit/). A lot (too).  But I have my own ideas about what patches to include.

Thanks to [imeyer](https://github.com/imeyer/runit-rpm) for doing most of the work to package this stuff.

## Building

```
yum -q -y install rpmdevtools git glibc-static
yum -q -y groupinstall "Development Tools"
git clone https://github.com/shore/runit-rpm runit-rpm
cd ./runit-rpm
./build.sh
sudo rpm -i ~/rpmbuild/RPMS/*/runit-*.rpm
```
