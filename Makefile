EXAMPLES := hello-world blink rs232-receive rs232-send rs485-receive rs485-send
PIO := pio

.PHONY: all $(EXAMPLES) generate clean

all: $(EXAMPLES)

$(EXAMPLES):
	$(PIO) run -d examples/$@

generate:
	python3 generate_boards.py
	python3 examples/generate_platformio_ini.py

clean:
	for dir in $(EXAMPLES); do \
		rm -rf examples/$$dir/.pio; \
	done
