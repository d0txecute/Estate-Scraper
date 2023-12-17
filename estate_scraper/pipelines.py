from itemadapter import ItemAdapter
import csv


class EstateScraperPipeline:
    def open_spider(self, spider):
        output_file_name = f'data/{spider.name}.csv'
        self.csv_file = open(output_file_name, 'w', newline='')
        
        fieldnames = [
            "Description", "Size", "Bedrooms", "Bathrooms", "Building Type", "Area", "Price"
        ]

        if spider.name == "opensooq-rent":
            fieldnames.append("Furnishing")

        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)
        self.csv_writer.writeheader()


    def process_item(self, item, spider):
        if spider.name == "opensooq-rent":
            self.csv_writer.writerow({
                "Description": item.get("description", ""),
                "Size": item.get("size", ""),
                "Bedrooms": item.get("bedroom", ""),
                "Bathrooms": item.get("bathroom", ""),
                "Furnishing": item.get("furnishing", ""),
                "Building Type": item.get("building_type", ""),
                "Area": item.get("area", ""),
                "Price": item.get("price", "")
            })
        else:
            self.csv_writer.writerow({
                "Description": item.get("description", ""),
                "Size": item.get("size", ""),
                "Bedrooms": item.get("bedroom", ""),
                "Bathrooms": item.get("bathroom", ""),
                "Building Type": item.get("building_type", ""),
                "Area": item.get("area", ""),
                "Price": item.get("price", "")
            })
            
        return item

    def close_spider(self, spider):
        self.csv_file.close()
