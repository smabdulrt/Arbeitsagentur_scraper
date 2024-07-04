# Arbeitsagentur Job Scraper

## Overview

This project is a web scraper designed to extract job listings and detailed job information from the German Federal Employment Agency (Arbeitsagentur) website. The scraper is built using Scrapy, a popular web scraping framework for Python. It navigates the job search API, handles CAPTCHA challenges, and collects job details such as company information, job titles, contact details, and more.

## Features

- Extracts job listings from the Arbeitsagentur job search API.
- Collects detailed job information including company name, job title, job details URL, contact person's name, gender, address, email, and phone number.
- Uses base64 encoding for company codes required by the API.
- Configurable headers and session management for making authenticated requests.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/arbeitsagentur-scraper.git
    cd arbeitsagentur-scraper
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Navigate to the project directory:
    ```sh
    cd arbeitsagentur-scraper
    ```

2. Run the scraper:
    ```sh
    scrapy crawl arbeitsagentur
    ```

## Configuration

### Custom Settings

The scraper comes with custom settings for Scrapy, which can be modified according to your needs:

- `ZYTE_SMARTPROXY_ENABLED`: Enable or disable the Zyte Smart Proxy.
- `ZYTE_SMARTPROXY_APIKEY`: Your Zyte Smart Proxy API key.
- `DOWNLOADER_MIDDLEWARES`: Middleware configuration for using Zyte Smart Proxy.

These settings can be found and modified in the `ArbeitsagenturSpider` class under the `custom_settings` attribute.

### Headers

The headers used for requests are defined in the `headers` attribute of the `ArbeitsagenturSpider` class. You may need to update these headers, especially the `User-Agent` and `Cookie`, to mimic a real browser session.

### Payload

The payload for the CAPTCHA request is defined in the `payload` attribute. Ensure the `sessionId` is updated if necessary.

## Spider Structure

### start_requests

This method initiates the scraping by sending a request to the job search API.

### parse

This method parses the response from the job search API, extracting job listings and initiating requests to fetch detailed job information.

### encode_to_base64

This utility method encodes a given string to base64 format, which is required by the API for company codes.

### parse_details

This method parses the detailed job information, including company details and job title, and initiates a request to handle the CAPTCHA challenge.

### parse_captcha

This method handles the CAPTCHA challenge by sending the required answers and session information, then proceeds to fetch additional job information.

### parse_info

This method parses the final detailed job information, including contact details and address, and yields the data.

## Output

The scraped data is stored in JSON format, containing the following fields:
- `company_name`: The name of the company offering the job.
- `job_Title`: The title of the job.
- `Detail_url`: The URL for the job details.
- `First Name`: The first name of the contact person.
- `Last Name`: The last name of the contact person.
- `Gender`: The gender of the contact person.
- `address`: The address of the company.
- `Email`: The email address of the contact person.
- `Contact_number`: The phone number of the contact person.

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```sh
    git push origin feature-branch
    ```
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.

---

Happy scraping!
