from setuptools import setup, find_packages

setup(
    name="user-recon",
    version="1.0.0",
    author="User Recon Team",
    author_email="contact@userrecon.io",
    description="AI-driven OSINT tool for username detection, similarity analysis, and cross-platform intelligence.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/user-recon",
    packages=find_packages(exclude=("tests", "data", "logs", "ci")),
    include_package_data=True,
    install_requires=[
        "requests>=2.28.0",
        "colorama>=0.4.6",
        "scikit-learn>=1.2.0",
        "numpy>=1.24.0",
        "pandas>=1.5.0",
        "redis>=4.5.0",
        "psutil>=5.9.0",
        "tqdm>=4.65.0",
    ],
    entry_points={
        "console_scripts": [
            "user-recon=user_recon.main:run",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
)
