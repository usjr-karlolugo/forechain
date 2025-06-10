import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-url-input',
  templateUrl: './url-input.component.html',
  styleUrls: ['./url-input.component.css']
})
export class UrlInputComponent {
  url: string = '';
  @Output() scrape = new EventEmitter<string>();

  onScrape() {
    if (this.url && this.url.trim()) {
      this.scrape.emit(this.url.trim());
    }
  }
}