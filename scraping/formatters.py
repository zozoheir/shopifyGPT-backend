import trafilatura
from datetime import datetime

date_format = '%Y-%m-%dT%H:%M:%S%z'


def month_diff(a, b):
    return (a.year - b.year) * 12 + a.month - b.month


def format_json(json_dict):
    # Exclude unwanted keys
    excluded_keys = ["body_html", "variants", "options"]

    # Start with an empty string
    formatted_string = ""

    for key, value in json_dict.items():
        # Check if the key is not in the excluded keys list
        if key not in excluded_keys:
            # Append the key-value pair to the formatted string
            formatted_string += f"- {key.capitalize()}: {value}\n"

    # Return the formatted string
    return formatted_string.strip()


# Clean up Nones.

def formatProductDict(product_dict):
    product_fields_to_remove = ['handle', 'updated_at', 'body_html', 'created_at',
                                'updated_at', 'vendor', 'images']

    # Strings to process: title, description, product_type, published_date, tags, options, variants
    variant_fields_to_remove = ['sku', 'requires_shipping', 'taxable', 'featured_image',
                                'position', 'product_id', 'created_at', 'updated_at']

    options_fields_to_remove = ['position']

    # Extract description
    product_dict['description'] = trafilatura.extract(product_dict['body_html'])

    # Extract published date
    datetime_object = datetime.strptime(product_dict['published_at'], date_format)
    today = datetime.today()
    diff_in_months = month_diff(today, datetime_object)
    published_date_string = datetime_object.strftime("%A, %B %-d %Y")
    if diff_in_months >= 12:
        years = diff_in_months // 12
        published_date_string += f", it's been available for more than {years} year{'s' if years > 1 else ''}"
    elif diff_in_months > 0:
        published_date_string += f", it's been available for {diff_in_months} month{'s' if diff_in_months > 1 else ''}"

    product_dict['tags'] = ", ".join([i.capitalize() for i in product_dict['tags']])

    # Process variants
    processed_variants_list = []
    for product_variant_dict in product_dict['variants']:

        if product_variant_dict['compare_at_price'] is None:
            product_variant_dict['compare_at_price'] = product_variant_dict['price']
        product_variant_dict['discount'] = round(
            1 - float(product_variant_dict['price']) / float(product_variant_dict['compare_at_price']), 2)
        if product_variant_dict['discount'] == 0:
            product_variant_dict['discount'] = "None"
        else:
            product_variant_dict['discount'] = "{:.0%}".format(product_variant_dict['discount'])

        processed_variants_list.append(
            {k: v for k, v in product_variant_dict.items() if k not in variant_fields_to_remove})

    product_dict['variants'] = processed_variants_list
    product_dict['published_at'] = published_date_string

    # Remove unwanted fields and rename fields
    product_dict_to_return = {k: v for k, v in product_dict.items() if k not in product_fields_to_remove}
    for i, p in enumerate(product_dict_to_return['variants']):
        variant_dict = {k: v for k, v in p.items() if k not in variant_fields_to_remove}
        #rename fields
        variant_dict['regular_price'] = variant_dict.pop('compare_at_price')
        product_dict_to_return['variants'][i] = variant_dict

    for i, p in enumerate(product_dict_to_return['options']):
        option_dict = {k: v for k, v in p.items() if k not in options_fields_to_remove}
        product_dict_to_return['options'][i] = option_dict

    full_product_description_string = string_format_product(product_dict_to_return)

    return product_dict_to_return, full_product_description_string


def dict_to_string(my_dict, indent=""):
    result = ''
    for key, value in my_dict.items():
        if value is not None:
            result += indent + f"- {key.capitalize().replace('_', ' ')}: {value}\n"
    return result


def string_format_variants(clean_product_dict, indent=""):
    indent = '    '
    variants_string = f'Product variants:\n'
    for variant_dict in clean_product_dict['variants']:
        # Set variant title
        variants_string = variants_string + indent+ variant_dict['title'] + ' Variant:\n'

        # Process options into key and string
        options = [variant_dict[i] for i in variant_dict.keys() if 'option' in i if variant_dict[i] is not None]
        variant_options_string = ', '.join(options)
        variant_dict = {k: v for k, v in variant_dict.items() if 'option' not in k}
        variant_dict['options'] = variant_options_string

        # Create string list
        variants_string = variants_string + dict_to_string(
            {k: v for k, v in variant_dict.items() if k not in ['title']},
            indent=indent+indent)

    return variants_string


def string_format_options(clean_product_dict, indent=""):
    options_string = 'Product options:\n'
    for option in clean_product_dict['options']:
        options_string = options_string + indent+ option['name'] + ' option:\n'
        options_string = options_string + dict_to_string(option, indent=indent+indent)
    return options_string

def string_format_product(clean_product_dict):
    product_string = 'Product information:\n'
    product_string = product_string + dict_to_string(
        {k: v for k, v in clean_product_dict.items() if k not in ['variants', 'options']})

    indent = '    '
    variables_string = string_format_variants(clean_product_dict, indent=indent)
    options_string = string_format_options(clean_product_dict, indent=indent)

    final_string = product_string + '\n' + variables_string + '\n' + options_string

    from pprint import pprint
    pprint(final_string)

    return final_string


