parse_excel:
	if [ -z "$(FILE)" ]; then \
		echo "Please provide the Excel file with FILE=<path>"; \
		exit 1; \
	fi
	python -c "from app.parser import parse_excel; parse_excel('$(FILE)')"
