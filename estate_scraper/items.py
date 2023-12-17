from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst


def get_price(txt):
    return txt.replace("OMR", "").replace(",", "").split()

def get_size(txt):
    return txt.replace("m2", "").split()

def get_bedroom(txt):
    return txt.replace("s", "").replace("Bedroom", "").split()

def get_bathroom(txt):
    return txt.replace("s", "").replace("Bathroom", "").replace("+", "").split()
    

class EstateItem(Item):
    description = Field(output_processor = TakeFirst())
    size = Field(
        input_processor = MapCompose(get_size),
        output_processor = TakeFirst()
    )
    
    bedroom = Field(
        input_processor = MapCompose(get_bedroom),
        output_processor = TakeFirst()
    )
    
    bathroom = Field(
        input_processor = MapCompose(get_bathroom),
        output_processor = TakeFirst()                 
    )
    
    furnishing = Field(output_processor = TakeFirst())
    building_type = Field(output_processor = TakeFirst())
    
    area = Field(output_processor = TakeFirst())
    
    price = Field(
        input_processor = MapCompose(get_price),
        output_processor = TakeFirst()
    )
    # link = Field()
    