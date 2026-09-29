Markdown

# Amplitude Data Extraction & S3 Loader

An automated pipeline to extract event data from the Amplitude Export API, decompress the files, and load the processed JSON output directly into an AWS S3 bucket.

## Features

- **Amplitude API Integration:** Connects to the Export API and retrieves zipped event data.
- **Decompression:** Extracts primary ZIP archives and recursively decompresses internal GZIP files.
- **Local Storage:** Saves extracted JSON data locally for intermediate processing.
- **AWS S3 Upload:** Automatically uploads extracted JSON files to Amazon S3 and cleans up local storage.
- **Logging:** Generates detailed execution logs in the `log/` directory for monitoring and debugging.

## Dependencies & Setup

- [requirements.txt](https://github.com/JadenMatt/DES8-Amplitude/blob/main/requirements.txt)

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
## .env setup

# Amplitude API Credentials

AMP_API_KEY="your_amplitude_api_key"

AMP_SECRET_KEY="your_amplitude_secret_key"

# AWS S3 Credentials

AWS_ACCESS_KEY="your_aws_access_key"

AWS_SECRET_ACCESS_KEY="your_aws_secret_key"

AWS_BUCKET_NAME="your_s3_bucket_name"

## Authors

Jaden Matthias

## License

This project is licensed under the MIT License - see [License](https://github.com/JadenMatt/DES8-Amplitude/blob/main/LICENSEfile) for details.'
