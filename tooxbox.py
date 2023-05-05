import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


# 要保存的分类列表
class ImageClassifier(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("尼式染色质量分类工具箱")
        self.master.geometry("1500x1200")
        self.categories = ["切片贴片", "包埋","切削","质量优秀"]        
        # 创建控件
        self.current_image_index = 0
        self.pathroot = r'G:\data\dataset\R03\Nissl'
        self.saveroot = r'C:\Users\SJ\Pictures'
        
        self.create_widgets()
        # 显示第一张图像
        self.makedir_path()
        self.show_image(self.current_image_index)

        
        
    def create_widgets(self):
        
         #创建进度区域
        self.category_label = tk.Label(self.master)
        self.category_label.pack()
        
   
    
        # 创建分类选择区域
        self.class_frame = tk.Frame(self.master)
        self.class_frame.pack(pady=10)

        self.class_button = tk.Button(self.class_frame, text="切片贴片", command=lambda: self.save_image("切片贴片"))
        self.class_button.pack(side="left", padx=5)
        self.class_button = tk.Button(self.class_frame, text="包埋",     command=lambda: self.save_image("包埋"))
        self.class_button.pack(side="left", padx=5)
        self.class_button = tk.Button(self.class_frame, text="切削",     command=lambda: self.save_image("切削"))
        self.class_button.pack(side="left", padx=5)
        self.class_button = tk.Button(self.class_frame, text="质量优秀", command=lambda: self.save_image("质量优秀"))
        self.class_button.pack(side="left", padx=5)        
        
        # 创建按钮区域
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)
        
        
        self.prev_button = tk.Button(self.button_frame, text="上一张", command=self.show_prev_image)
        self.prev_button.pack(side="left", padx=5)
        
        self.next_button = tk.Button(self.button_frame, text="下一张", command=self.show_next_image)
        self.next_button.pack(side="left", padx=5)
        # 创建图像显示区域
        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=10)
        
       
    def show_image(self, index):
        # 加载图像
        image_path = self.get_image_path(index)
        print(image_path)
        image = Image.open(image_path)
        
        # 缩放图像
        max_width = 1000
        max_height = 1000
        
        if image.width > max_width:
            image = image.resize((max_width, int(image.height / image.width * max_width)))
        if image.height > max_height:
            image = image.resize((int(image.width / image.height * max_height), max_height))
        
        # 显示图像
        photo = ImageTk.PhotoImage(image)
        
        self.image_label.configure(image=photo)
        self.image_label.image = photo
        
        self.category_label.configure(text="进度:{:.2f}%--{}/{}".format(100*self.current_image_index/self.get_num_images(),self.current_image_index,self.get_num_images(),))
    
    def show_prev_image(self):
        # 显示上一张图像
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image(self.current_image_index)
    
    def show_next_image(self):
        # 显示下一张图像
        if self.current_image_index < self.get_num_images() - 1:
            self.current_image_index += 1
            self.show_image(self.current_image_index)

    def makedir_path(self):
        for category in self.categories:
            category_path = os.path.join(self.saveroot, category)
            if not os.path.isdir(category_path):
                os.makedirs(category_path)                
    def save_image(self,category):
        # 保存当前图像，如果分类目录不存在则创建
        image_path = self.get_image_path(self.current_image_index)
        category_path = os.path.join(self.saveroot,category)
        
        image_name = os.path.basename(image_path)
        save_path = os.path.join(category_path, image_name)
        
        with open(image_path, "rb") as f:
            with open(save_path, "wb") as s:
                s.write(f.read())
        
        print("图像已保存到：", save_path)
    
    def get_num_images(self):
        # 获取图像数量
        num_images = 0
        
        for file in os.listdir(self.pathroot):
            if file.endswith(".jpg") or file.endswith(".png"):
                num_images += 1
        
        return num_images
    
    def get_image_path(self, index):
        # 获取指定索引的图像路径
        for i, file in enumerate(sorted(os.listdir(self.pathroot))):
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".tif") :
                if i == index:
                    return os.path.join(self.pathroot, file)
        return None
        
root = tk.Tk()
app = ImageClassifier(root)  
app.mainloop()
