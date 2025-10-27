# Define the Backend Service (connects the LB to your VMs via the Instance Group)
resource "google_compute_backend_service" "web_backend" {
  name        = "web-backend-service"
  protocol    = "HTTP"
  port_name   = "http"
  timeout_sec = 10
  
  # Health Check configuration
  health_checks = [google_compute_health_check.http_health_check.id]

  # Add the Managed Instance Group (MIG) as the backend
  backend {
    group = google_compute_instance_group_manager.lb_mig.instance_group # Assumes you have a MIG resource named 'lb_mig'
  }
}

# Define the Health Check (ensures traffic only goes to healthy VMs)
resource "google_compute_health_check" "http_health_check" {
  name             = "http-basic-check"
  check_interval_sec = 5
  timeout_sec        = 5
  healthy_threshold  = 2
  unhealthy_threshold = 10
  
  http_health_check {
    port         = 80
    request_path = "/"
  }
}

# Define the URL Map (routes requests to the correct Backend Service)
resource "google_compute_url_map" "web_map" {
  name            = "web-url-map"
  default_service = google_compute_backend_service.web_backend.id
}

# Define the Target HTTP Proxy (receives traffic and forwards it based on the URL Map)
resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "http-target-proxy"
  url_map = google_compute_url_map.web_map.id
}

# Reserve a Global IP Address for the Load Balancer Frontend
resource "google_compute_global_address" "lb_static_ip" {
  name = "web-lb-ip"
}

# Define the Global Forwarding Rule (Frontend: entry point for external traffic)
resource "google_compute_global_forwarding_rule" "http_forwarding_rule" {
  name       = "http-forwarding-rule"
  ip_protocol = "TCP"
  port_range = "80"
  target     = google_compute_target_http_proxy.http_proxy.id
  ip_address = google_compute_global_address.lb_static_ip.id
}

# Output the IP Address so you can access the website
output "load_balancer_ip" {
  value       = google_compute_global_address.lb_static_ip.address
  description = "The external IP address of the HTTP Load Balancer."
}
