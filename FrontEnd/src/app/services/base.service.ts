import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BaseEntity } from '../models/baseEntity';
import { Injectable } from '@angular/core';
import { KeywordAnalysis } from '../models/keywordAnalysis';
@Injectable({
  providedIn: 'any',
})
export class BaseService {

  public baseUrl: string = "http://127.0.0.1:5000/";
  constructor(protected http: HttpClient) {
  }

  get(url: string, body: any) {
    return this.http.get<KeywordAnalysis>(this.baseUrl + url, body);
  }

  post(url: string, data: any): Observable<BaseEntity> {
    return this.http.post<BaseEntity>(this.baseUrl + url, data);
  }
}
