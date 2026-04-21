Для выполнения задания вам понадобится изображение cattle.jpg. Скачайте его.  
Импортируйте предобученную модель "microsoft/swin-tiny-patch4-window7-224" с помощью библиотеки transformers и классифицируйте изображение. Числовой идентификатор предсказанного класса разместите в переменной predicted_class_idx. 
Выполните задание локально, затем сверьтесь с ожидаемым выводом и авторским решением. 

from transformers import AutoImageProcessor, AutoModelForImageClassification

# Загрузка модели и препроцессора
model_name = "microsoft/swin-base-patch4-window12-384"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)