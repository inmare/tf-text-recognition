from pdf2image import convert_from_path

file_name = "random-ascii"

images = convert_from_path(f"./pdf/{file_name}.pdf", dpi=300, grayscale=True)

for i, page in enumerate(images):
	page.save(f"./image/{file_name}.jpg", "JPEG", quality=25)