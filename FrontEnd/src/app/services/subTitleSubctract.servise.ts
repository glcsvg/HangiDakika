import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { SubTitleSubctract } from '../models/subTitleSubctract';
@Injectable({
    providedIn: 'any',
})
export class SubTitleSubctractService {

    public baseUrl: string = "http://127.0.0.1:5000/";
    constructor(protected http: HttpClient) {
    }

    get(url: string, body: any) {
        return this.http.get<SubTitleSubctract>(this.baseUrl + url, body);
    }

    post(url: string, data: any): Observable<SubTitleSubctract> {
        return this.http.post<SubTitleSubctract>(this.baseUrl + url, data);
    }
}
