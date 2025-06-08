import { Component, Input } from '@angular/core';
import { InsightResponse } from '../../models/insight-response';
@Component({
  selector: 'app-predicted-insights',
  templateUrl: './predicted-insights.component.html',
  styleUrl: './predicted-insights.component.css'
})
export class PredictedInsightsComponent {
  @Input() loading = false;
  @Input() error = false;
  @Input() insightText: InsightResponse | null = null;
}
