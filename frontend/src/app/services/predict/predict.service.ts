import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { InsightResponse } from '../../models/insight-response';
@Injectable({
  providedIn: 'root'
})
export class PredictService {
  private apiUrl = 'http://127.0.0.1:8005/predict/alert/';
  private urlApi = 'http://127.0.0.1:8005/predict/url/';

  constructor(private http: HttpClient) {}

  predictInsights(summary: string): Observable<InsightResponse> {
    return this.http.post<InsightResponse>(this.apiUrl, { text: summary });
  }

  predictInsightsFromUrl(url: string): Observable<InsightResponse> {
    return this.http.post<InsightResponse>(this.urlApi, { url });
  }
}
