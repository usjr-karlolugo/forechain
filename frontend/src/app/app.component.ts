import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
  currentRoute: 'articles' | 'statistics' = 'articles';

  constructor(private router: Router) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        if (event.url.includes('statistics')) {
          this.currentRoute = 'statistics';
        } else {
          this.currentRoute = 'articles';
        }
      }
    });
  }

  onRouteChange(route: 'articles' | 'statistics') {
    this.router.navigateByUrl(`/${route}`);
  }
}
