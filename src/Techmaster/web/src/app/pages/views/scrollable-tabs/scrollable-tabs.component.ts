import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'scrollable-tabs',
  templateUrl: './scrollable-tabs.component.html',
  styleUrls: ['./scrollable-tabs.component.css']
})
export class ScrollableTabsComponent implements OnInit {
  @Input() tabs: any;
  selectedIndex = 0;
  abc: string | undefined;
  leftTabIdx = 0;
  atStart = true;
  atEnd = false
  @Output() emitSelectedTab = new EventEmitter()
  constructor() { }

  ngOnInit() {
    const responseTab = JSON.parse(localStorage.getItem('tabView') || '{}');
    if (Object.keys(responseTab).length > 0) {
      localStorage.setItem("viewTabLS", 'true');
      this.abc = `translateX(0px)`
      this.selectedIndex = (responseTab["id"] - 1)
      this.emitSelectedTab.emit(this.tabs[(responseTab["id"] - 1)])
      this.scrollTab((responseTab["id"] - 1) - this.leftTabIdx - 1)
    } else {
      localStorage.setItem("viewTabLS", 'false');
      this.emitSelectedTab.emit(this.tabs[0])
      this.abc = `translateX(0px)`
    }
  }

  selectTab(index: any) {
    localStorage.setItem("viewTabLS", 'false');
    this.selectedIndex = index
    this.emitSelectedTab.emit(this.tabs[index])
    this.scrollTab(index - this.leftTabIdx - 1)
  }

  scrollTab(x: any) {
    if (this.atStart && x < 0 || this.atEnd && x > 0) {
      return
    }
    this.leftTabIdx = this.leftTabIdx + x
    this.abc = `translateX(${(this.leftTabIdx) * -140}px)`
    this.atStart = this.leftTabIdx === 0
    this.atEnd = this.leftTabIdx === this.tabs.length - 1
  }

}