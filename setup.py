import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="haar_face_detection",
    version="0.0.1",
    author="Ivan Matskevich",
    author_email="matskevichivan98@gmail.com",
    description="A small face detection package",
    url="https://github.com/Matskevichivan/Haar_face_detection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
