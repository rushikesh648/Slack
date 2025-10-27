# Configure the Google Cloud provider
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# 1. Resource: Google Compute Instance (Virtual Machine)
resource "google_compute_instance" "web_server_vm" {
  # Change these variables to match your project needs
  name         = "web-server-instance"
  machine_type = "e2-medium"
  zone         = "us-central1-a"
  tags         = ["http-server", "web-server"]

  # Define the Boot Disk
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 10
    }
  }

  # Define the Network Interface
  network_interface {
    network = "default"
    access_config {
      # This block adds an external IP address
    }
  }

  # 2. Startup Script (to install a basic web server)
  metadata_startup_script = <<-EOF
    #!/bin/bash
    sudo apt update
    sudo apt install -y apache2
    echo "<h1>Page served from: $(hostname)</h1>" | sudo tee /var/www/html/index.html
    sudo systemctl enable apache2
    sudo systemctl start apache2
  EOF
}

# 3. Firewall Rule to allow HTTP traffic (port 80)
resource "google_compute_firewall" "allow_http" {
  name    = "allow-http-80"
  network = "default"
  
  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
  
  source_ranges = ["0.0.0.0/0"]
  # The firewall rule only applies to instances with this tag (set above)
  target_tags   = ["http-server"]
}

# 4. Output the external IP address of the deployed VM
output "external_ip" {
  value = google_compute_instance.web_server_vm.network_interface[0].access_config[0].nat_ip
  description = "The external IP address of the VM instance."
}
