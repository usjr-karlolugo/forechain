import { Component, OnInit, Renderer2 } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AlertService } from '../alert.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {
  alerts: any[] = [];
  objectKeys = Object.keys;

  constructor(
    private alertService: AlertService,
    private renderer: Renderer2  // Inject Renderer2
  ) {}

  ngOnInit(): void {
    this.alertService.getAlerts().subscribe({
      next: (data) => {
        // Sort the alerts by created_at in descending order (latest first)
        this.alerts = data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
      },
      error: (err) => console.error('Error loading alerts', err),
    });
  }

  // Method to open the article in a new tab
  openLink(url: string): void {
    window.open(url, '_blank');
  }
}
