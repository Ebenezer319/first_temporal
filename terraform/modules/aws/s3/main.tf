resource "aws_s3_bucket" "example" {
  bucket = "my-tf-test-bucket"

  tags = {
    Environment = var.tag_environment_name
    Maintainer  = var.tag_maintainer
    Name        = var.tag_name
    Run_always  = var.tag_run_always
    UniqueID    = var.tag_uniqueid
  }
}

resource "aws_s3_bucket_acl" "bucket_acl" {
    bucket = aws_s3_bucket.bucket.id
    acl    = var.bucket_acl
}

resource "aws_s3_bucket_versioning" "bucket_version" {
    bucket = aws_s3_bucket.bucket.id

    versioning_configuration {
      status = "Enabled"
    }
}

resource "aws_s3_bucket_notification" "bucket_notification_config" {
    bucket = aws_s3_bucket.bucket.id

    queue {
      queue_arn     = var.notification_queue_arn
      events        = ["s3:ObjectCreated:*"]
      filter_prefix = var.notification_filter_prefix
    }

    depends_on = [ aws_s3_bucket.bucket, var.queue ]
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encrypt" {
    bucket = aws_s3_bucket.bucket.id

    rule {
        apply_server_side_encryption_by_default {
          sse_algorithm = "aws:AES256"
        }
    }
}

resource "aws_s3_bucket_public_access_block" "bucket_public_access_block" {
    bucket                  = aws_s3_bucket.id
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
}