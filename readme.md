# OS Environment
we need macOS or Linux for all code

for Windows , can only run calculate.py and transform.py  and qt5/main.py on it

# Environment Config
we need anaconda

conda create -n plant_phenotype python=3.9

conda activate plant_phenotype

pip install -r requirements.txt

pip3 install torch torchvision torchaudio

python -m pip install pyyaml==5.1

pip install 'git+https://github.com/facebookresearch/detectron2.git@5aeb252b194b93dc2879b4ac34bc51a31b5aee13'

tips: use VPN to build the env or use -i https://pypi.tuna.tsinghua.edu.cn/simple/ for pip install

then can run all my code

# Result

![活体植株实例分割](resources/%E5%8E%9F%E5%A7%8B%E6%A4%8D%E6%A0%AA%E5%AE%9E%E4%BE%8B%E5%88%86%E5%89%B2%E7%BB%93%E6%9E%9C%E6%B8%B2%E6%9F%93%E5%9B%BE.png)