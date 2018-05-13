#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 16:44:59 2018

@author: owen
"""

from elasticsearch import Elasticsearch


class ElasticService:
    def __init__(self):
        self.es = Elasticsearch()
        
    def save_to_database(self, index, doc_type, data):
        if isinstance(data, list):
            for d in data:
                print d['id']
                if d['id'] is None:
                    continue
                else:
                    self.es.index(
                        index=index,
                        doc_type=doc_type,
                        id=d['id'],
                        body=d)
        else:
            self.es.index(
                index=index,
                doc_type=doc_type,
                id=data['id'],
                body=data)
            
    def get_from_database(self, index, doc_type, elastic_id):
        elastic_response = self.es.get(
            index=index, 
            doc_type=doc_type, 
            id=elastic_id)
        return elastic_response['_source']
        
    def search_database(self, index, query):
        elastic_response = self.es.search(
            index='properties',
            body={"query": {"match_all": {}}})
        search_results = []
        for hit in elastic_response['hits']['hits']:
            search_results.append(
                hit['_source'])
        return search_results
