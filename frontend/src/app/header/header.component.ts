import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
})
export class HeaderComponent {
  @Input() activeRoute: 'articles' | 'statistics' = 'articles';
  @Output() navigate = new EventEmitter<'articles' | 'statistics'>();

  navigateTo(route: 'articles' | 'statistics') {
    this.navigate.emit(route);
  }

  onNavigate(route: 'articles' | 'statistics', event: Event) {
    event.preventDefault(); // stops page from jumping to top
    this.activeRoute = route;
    this.navigateTo(route);
  }
}