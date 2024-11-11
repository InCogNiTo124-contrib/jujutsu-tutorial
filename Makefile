.PHONY: default

default:
	nohup mdbook serve --watcher=native > /dev/null &
