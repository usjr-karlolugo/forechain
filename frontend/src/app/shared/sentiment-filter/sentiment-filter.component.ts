import { Component, EventEmitter, Output } from '@angular/core';
@Component({
  selector: 'app-sentiment-filter',
  templateUrl: './sentiment-filter.component.html',
  styleUrl: './sentiment-filter.component.css'
})
export class SentimentFilterComponent {
  selectedSentiment: string = 'all';

  @Output() sentimentChange = new EventEmitter<string>();

  onSentimentChange(event: Event) {
    const value = (event.target as HTMLSelectElement).value;
    this.selectedSentiment = value;
    this.sentimentChange.emit(value);
  }
}
