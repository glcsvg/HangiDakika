import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { KeywordAnalysis } from '../models/keywordAnalysis';
@Injectable({
  providedIn: 'any',
})
export class KeywordAnalysisService {

  public baseUrl: string = "http://127.0.0.1:5000/";
  constructor(protected http: HttpClient) {
  }

  get(url: string, body: any) {
    debugger
    return this.http.get<KeywordAnalysis>(this.baseUrl + url, body);
  }

  post(url: string, data: any): Observable<KeywordAnalysis> {
    return this.http.post<KeywordAnalysis>(this.baseUrl + url, data);
  }
}

