import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
})
export class HeaderComponent {
  @Input() activeRoute: 'articles' | 'statistics' | 'profile' = 'articles';
  @Output() navigate = new EventEmitter<'articles' | 'statistics' | 'profile'>();

  navigateTo(route: 'articles' | 'statistics' | 'profile') {
    this.navigate.emit(route);
  }

  onNavigate(route: 'articles' | 'statistics' | 'profile', event: Event) {
    event.preventDefault();
    this.activeRoute = route;
    this.navigateTo(route);
  }
}