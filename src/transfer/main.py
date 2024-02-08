from client import GoogleCloudStorageClient


bucket_name = "sgb-pdf-store"  # 保存先のバケット名
destination_blob_name = "guide.pdf"  # 保存先となるバケット内でのファイルパス
local_file_path = "./data/guide.pdf"  # 保存したいファイルパス

GoogleCloudStorageClient.upload_file(
    bucket_name, destination_blob_name, local_file_path
)
