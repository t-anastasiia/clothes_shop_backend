from django.db import models
from django.core.exceptions import ValidationError

# --- Вспомогательные перечисления ---

class ProductType(models.TextChoices):
    CLOTHES = 'clothes', 'Одежда'
    SHOES = 'shoes', 'Обувь'

class SizeType(models.TextChoices):
    CLOTHES = 'clothes', 'Одежда'
    SHOES = 'shoes', 'Обувь'

class ClothesCategory(models.TextChoices):
    TOP = 'top', 'Верхняя'
    BOTTOM = 'bottom', 'Нижняя'

class ShoesCategory(models.TextChoices):
    SANDALS = 'sandals', 'Сандалии'
    SLIPPERS = 'slippers', 'Тапки'
    SNEAKERS = 'sneakers', 'Кроссовки'
    KEDS = 'keds', 'Кеды'

# --- Модели ---

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=50)
    size_type = models.CharField(
        max_length=10,
        choices=ProductType.choices,
        default=ProductType.CLOTHES
    )

    def __str__(self):
        return f"{self.name} ({self.get_size_type_display()})"
    
class Tag(models.Model):
    """
    Теги для рекомендательной системы.
    Например: "casual", "sport", "classic" и т.д.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    """
    Модель товара.
    - id: создаётся автоматически (primary key)
    - colors: список доступных расцветок (ManyToMany к Color)
    - sizes: список доступных размеров (ManyToMany к Size)
    - tags: список тегов для рекомендательной системы (ManyToMany к Tag)
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    product_type = models.CharField(
        max_length=10,
        choices=ProductType.choices,
        default=ProductType.CLOTHES
    ) 
    subtype = models.CharField(max_length=20, blank=False, null=False)
    colors = models.ManyToManyField(Color, related_name='products')
    sizes = models.ManyToManyField(Size, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products')

    def __str__(self):
        return self.name
    
    def clean(self):
        """
        Валидация:
         1. Проверяем, что размеры соответствуют общему типу товара.
         2. Проверяем, что subtype соответствует выбранному product_type.
        """
        # Проверка размеров
        invalid_sizes = self.sizes.exclude(size_type=self.product_type)
        if invalid_sizes.exists():
            raise ValidationError(
                f"У товара типа '{self.get_product_type_display()}' "
                f"некорректные размеры: {', '.join(str(s) for s in invalid_sizes)}"
            )

        # Проверка подтипа товара
        if self.product_type == ProductType.CLOTHES:
            valid_subtypes = [choice[0] for choice in ClothesCategory.choices]
            if self.subtype not in valid_subtypes:
                raise ValidationError(
                    f"Для одежды subtype должен быть одним из {valid_subtypes}"
                )
        elif self.product_type == ProductType.SHOES:
            valid_subtypes = [choice[0] for choice in ShoesCategory.choices]
            if self.subtype not in valid_subtypes:
                raise ValidationError(
                    f"Для обуви subtype должен быть одним из {valid_subtypes}"
                )