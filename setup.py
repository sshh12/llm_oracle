from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="llm_oracle",
    version="0.0.0",
    description="",
    url="https://github.com/sshh12/llm_oracle",
    author="Shrivu Shankar",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
)
