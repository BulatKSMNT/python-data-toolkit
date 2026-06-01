import csv, sys, os, requests, re
from collections import defaultdict, Counter
from bs4 import BeautifulSoup 
from pprint import pprint
from statistics import mean, median, variance

import pytest
#еще нужно установить модуль pytest-mock для корректной работы тестов

class Movies:
    def __init__(self, path_to_the_file):
        if not os.path.exists(path_to_the_file):
            raise Exception("Invalid path")
        else :
            self.movies = []
            with open (path_to_the_file, encoding='utf-8') as file:
                 reader = csv.DictReader(file)
                 for i, row in enumerate(reader):
                     if i>=1000:
                         break
                     self.movies.append(row)  

    def dist_by_release(self):
        release_years = {} 
        for row in self.movies:
            title = row['title']
            match = re.search(r'\((\d{4})\)', title)
            if match:
                year = int(match.group(1))
                if year in release_years:
                    release_years[year] += 1
                else:
                    release_years[year] = 1

        release_years = dict(sorted(release_years.items(), key=lambda x: x[1], reverse=True))
        return release_years

    def dist_by_genres(self):
        genre_counter = Counter()

        for row in self.movies:
            genre = row['genres'].split('|')
            genre_counter.update(genre)
            
        genres = dict(genre_counter.most_common())
        return genres
        
    def most_genres(self, n):
        movies = {}
        for row in self.movies:
            title = row['title']
            genre = row['genres'].split('|')
            count = len(genre)
            movies[title] = count
        movies = dict(sorted(movies.items(), key=lambda x: x[1], reverse=True)[:n])
        return movies

class Links:
    def __init__(self, links_path, movies_path):
        if not os.path.exists(links_path) or not os.path.exists(movies_path):
            raise Exception("Invalid path to file(s)")
        
        links_data = {}
        with open(links_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 1000:
                    break
                links_data[row['movieId']] = row['imdbId']

        self.data = []
        with open(movies_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 1000:
                    break
                movie_id = row['movieId']
                if movie_id in links_data:
                    self.data.append({
                        'movieId': movie_id,
                        'title': row['title'],
                        'genres': row['genres'],
                        'imdbId': links_data[movie_id]
                    })
                     
    def get_imdb(self, list_of_titles, list_of_fields):
        imdb_info = []

        for title in list_of_titles:
            movie = next((m for m in self.data if m['title'] == title), None)
            if not movie:
                continue

            imdb_id = movie['imdbId']
            url = f'https://www.imdb.com/title/tt{imdb_id.zfill(7)}/'

            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Accept-Language': 'en-US,en;q=0.9'
                }
                response = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')

                data = []
                for field in list_of_fields:
                    field_lower = field.lower()

                    if field_lower == 'director':
                        director_tag = soup.find('li', {'data-testid': 'title-pc-principal-credit'})
                        name_tag = director_tag.find('a') if director_tag else None
                        value = name_tag.text.strip() if name_tag else 'N/A'

                    elif field_lower == 'budget':
                        box_office = soup.find('li', attrs={'data-testid': 'title-boxoffice-budget'})
                        spans = box_office.find_all('span') if box_office else []
                        value = spans[1].text.strip() if len(spans) >= 2 else 'N/A'

                    elif field_lower == 'cumulative worldwide gross':
                        gross_tag = soup.find('li', attrs={'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
                        spans = gross_tag.find_all('span') if gross_tag else []
                        value = spans[1].text.strip() if len(spans) >= 2 else 'N/A'

                    elif field_lower == 'runtime':
                        runtime_tag = soup.find('li', attrs={'data-testid': 'title-techspec_runtime'})
                        value = runtime_tag.find('div', class_='ipc-metadata-list-item__content-container').text.strip() if runtime_tag else 'N/A'

                    else:
                        value = 'N/A'

                    data.append(value)

            except Exception as e:
                print(f"Error fetching data for {title}: {e}")
                data = ['ERROR'] * len(list_of_fields)

            imdb_info.append([title] + data)

        return sorted(imdb_info, key=lambda x: x[0], reverse=True)


    def parse_money(self, value):
        if not value or 'N/A' in value or 'ERROR' in value:
            return 0
        value = re.sub(r'[^\d]', '', value)
        return int(value) if value else 0


    def parse_runtime(self, value):
        if not value or 'N/A' in value:
            return 0
        hours = 0
        minutes = 0
        h_match = re.search(r'(\d+)\s*h', value)
        m_match = re.search(r'(\d+)\s*m', value)
        if h_match:
            hours = int(h_match.group(1))
        if m_match:
            minutes = int(m_match.group(1))
        return hours * 60 + minutes

        
    def top_directors(self, n):
        data = self.get_imdb([m['title'] for m in self.data], ['Director'])
        counter = Counter()
        for row in data:
            director = row[1]
            if director not in ['N/A', 'ERROR']:
                counter[director] += 1
        return dict(counter.most_common(n))
        
    def most_expensive(self, n):
        data = self.get_imdb([m['title'] for m in self.data], ['Budget'])
        result = {}
        for row in data:
            title = next((m['title'] for m in self.data if m['title'] == row[0]), 'Unknown')
            budget = self.parse_money(row[1])
            if budget > 0:
                result[title] = budget
        sorted_result = sorted(result.items(), key=lambda x: (x[1], x[0]), reverse=True)
        return {k: v for k, v in sorted_result[:n]}


        
    def most_profitable(self, n):
        data = self.get_imdb([m['title'] for m in self.data], ['Budget', 'Cumulative Worldwide Gross'])
        result = {}
        for row in data:
            title = next((m['title'] for m in self.data if m['title'] == row[0]), 'Unknown')
            budget = self.parse_money(row[1])
            gross = self.parse_money(row[2])
            profit = gross - budget
            if profit > 0:
                result[title] = profit
        sorted_result = sorted(result.items(), key=lambda x: (x[1], x[0]), reverse=True)
        return {k: v for k, v in sorted_result[:n]}

        
    def longest(self, n):
        data = self.get_imdb([m['title'] for m in self.data], ['Runtime'])
        result = {}
        for row in data:
            title = next((m['title'] for m in self.data if m['title'] == row[0]), 'Unknown')
            runtime = self.parse_runtime(row[1])
            if runtime > 0:
                result[title] = runtime
        sorted_result = sorted(result.items(), key=lambda x: (x[1], x[0]), reverse=True)
        return {k: v for k, v in sorted_result[:n]}


        
    def top_cost_per_minute(self, n):
        data = self.get_imdb([m['title'] for m in self.data], ['Budget', 'Runtime'])
        result = {}
        for row in data:
            title = next((m['title'] for m in self.data if m['title'] == row[0]), 'Unknown')
            budget = self.parse_money(row[1])
            runtime = self.parse_runtime(row[2])
            if runtime > 0:
                cost_per_min = round(budget / runtime, 2)
                result[title] = cost_per_min
        sorted_result = sorted(result.items(), key=lambda x: (x[1], x[0]), reverse=True)
        return {k: v for k, v in sorted_result[:n]}

class Ratings:
    def __init__(self, ratings_path, movies_path):
        if not os.path.exists(ratings_path) or not os.path.exists(movies_path):
            raise Exception("Invalid path")

        self.ratings = []
        with open(ratings_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i >= 1000:
                    break
                self.ratings.append({
                    'userId': row['userId'],
                    'movieId': row['movieId'],
                    'rating': float(row['rating']),
                    'timestamp': int(row['timestamp'])
                })

        self.movie_titles = {}
        with open(movies_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.movie_titles[row['movieId']] = row['title']

    class Movies:
        def __init__(self, parent):
            self.parent = parent

        def dist_by_rating(self):
            counter = Counter()
            for r in self.parent.ratings:
                rating = round(r['rating'], 1)
                counter[rating] += 1
            return dict(sorted(counter.items()))

        def top_by_num_of_ratings(self, n):
            counter = Counter()
            for r in self.parent.ratings:
                counter[r['movieId']] += 1
            top = counter.most_common(n)
            return {self.parent.movie_titles.get(mid, mid): count for mid, count in top}

        def top_by_ratings(self, n, metric='average'):
            rating_map = defaultdict(list)
            for r in self.parent.ratings:
                rating_map[r['movieId']].append(r['rating'])

            result = {}
            for mid, values in rating_map.items():
                value = mean(values) if metric == 'average' else median(values)
                result[self.parent.movie_titles.get(mid, mid)] = round(value, 2)

            return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:n])

        def top_controversial(self, n):
            rating_map = defaultdict(list)
            for r in self.parent.ratings:
                rating_map[r['movieId']].append(r['rating'])

            result = {}
            for mid, values in rating_map.items():
                if len(values) >= 2:
                    result[self.parent.movie_titles.get(mid, mid)] = round(variance(values), 2)

            return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:n])


    class Users(Movies):
        def __init__(self, parent):
            super().__init__(parent)

        def dist_by_num_of_ratings(self):
            counter = Counter()
            for r in self.parent.ratings:
                counter[r['userId']] += 1
            return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

        def dist_by_avg_or_median(self, metric='average'):
            rating_map = defaultdict(list)
            for r in self.parent.ratings:
                rating_map[r['userId']].append(r['rating'])

            result = {}
            for uid, values in rating_map.items():
                val = mean(values) if metric == 'average' else median(values)
                result[uid] = round(val, 2)

            return dict(sorted(result.items(), key=lambda x: x[1]))

        def top_controversial_users(self, n):
            from statistics import variance
            rating_map = defaultdict(list)
            for r in self.parent.ratings:
                rating_map[r['userId']].append(r['rating'])

            result = {}
            for uid, values in rating_map.items():
                if len(values) >= 2:
                    result[uid] = round(variance(values), 2)

            return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:n])

class Tags:
    def __init__(self, path_to_the_file):
        if not os.path.exists(path_to_the_file):
            raise Exception("Invalid path")
        else :
            self.tags = []
            with open (path_to_the_file, encoding='utf-8') as file:
                 reader = csv.DictReader(file)
                 for i, row in enumerate(reader):
                     if i>=1000:
                         break
                     self.tags.append(row)  

    def most_words(self, n):
        seen = set()
        word_counts = {}

        for row in self.tags:
            tag = row['tag'].strip()
            if tag not in seen:
                seen.add(tag)
                word_count = len(tag.split())
                word_counts[tag] = word_count
        sorted_tags = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [tag for tag, _ in sorted_tags[:n]]

    def longest(self, n):
        seen = set()
        big_tags = {}

        for row in self.tags:
            tag = row['tag'].strip()
            if tag not in seen:
                seen.add(tag)
                big_tags[tag] = len(tag)

        sorted_tags = sorted(big_tags.items(), key=lambda x: x[1], reverse=True)
        return [tag for tag, _ in sorted_tags[:n]]


    def most_words_and_longest(self, n):

        tags_by_words = self.most_words(n)
        tags_by_length = self.longest(n)

        big_tags = set(tags_by_words) & set(tags_by_length)

        return sorted(big_tags)
        
    def most_popular(self, n):
        popular_tags = {}
        for row in self.tags:
            tag = row['tag'].strip()
            if tag in popular_tags:
                popular_tags[tag] += 1
            else:
                popular_tags[tag] = 1
        sorted_pop_tags = sorted(popular_tags.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_pop_tags[:n])
        
    def tags_with(self, word):
        seen = set()
        word = word.lower()
        tags_with_word ={}
        for row in self.tags:
            tag = row['tag'].strip()
            if word in tag.lower(): 
                seen.add(tag) 

        return sorted(seen)


class TestMoviesExtended:
    @pytest.fixture
    def sample_data(self, tmp_path):
        data = [
            {"movieId": "1", "title": "Film A (2000)", "genres": "Action|Adventure"},
            {"movieId": "2", "title": "Film B (2001)", "genres": "Comedy|Romance"},
            {"movieId": "3", "title": "Film C (2000)", "genres": "Action|Drama|Thriller"},
            {"movieId": "4", "title": "Film D (2002)", "genres": "Drama"},
        ]
        path = tmp_path / "movies.csv"
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["movieId", "title", "genres"])
            writer.writeheader()
            writer.writerows(data)
        return path

    def test_dist_by_release(self, sample_data):
        movies = Movies(sample_data)
        result = movies.dist_by_release()
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, int) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_dist_by_genres(self, sample_data):
        movies = Movies(sample_data)
        result = movies.dist_by_genres()
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_most_genres(self, sample_data):
        movies = Movies(sample_data)
        result = movies.most_genres(2)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

class TestLinksExtended:
    @pytest.fixture
    def sample_data(self, tmp_path):
        links_data = [
            {"movieId": "1", "imdbId": "0000001", "tmdbId": ""},
            {"movieId": "2", "imdbId": "0000002", "tmdbId": ""},
            {"movieId": "3", "imdbId": "0000003", "tmdbId": ""},
        ]
        movies_data = [
            {"movieId": "1", "title": "Film A", "genres": "Action"},
            {"movieId": "2", "title": "Film B", "genres": "Comedy"},
            {"movieId": "3", "title": "Film C", "genres": "Drama"},
        ]
        
        links_path = tmp_path / "links.csv"
        movies_path = tmp_path / "movies.csv"
        
        with open(links_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["movieId", "imdbId", "tmdbId"])
            writer.writeheader()
            writer.writerows(links_data)
            
        with open(movies_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["movieId", "title", "genres"])
            writer.writeheader()
            writer.writerows(movies_data)
            
        return links_path, movies_path

    def test_top_directors(self, sample_data, mocker):
        links_path, movies_path = sample_data
        links = Links(links_path, movies_path)
        
        # Мокируем запросы к IMDB
        mocker.patch.object(Links, 'get_imdb', return_value=[
            ["Film A", "Director X"],
            ["Film B", "Director Y"],
            ["Film C", "Director X"]
        ])
        
        result = links.top_directors(2)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_most_expensive(self, sample_data, mocker):
        links_path, movies_path = sample_data
        links = Links(links_path, movies_path)
        
        mocker.patch.object(Links, 'get_imdb', return_value=[
            ["Film A", "$1,000,000"],
            ["Film B", "$500,000"],
            ["Film C", "$2,000,000"]
        ])
        
        result = links.most_expensive(2)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_most_profitable(self, sample_data, mocker):
        links_path, movies_path = sample_data
        links = Links(links_path, movies_path)
        
        mocker.patch.object(Links, 'get_imdb', return_value=[
            ["Film A", "$1,000,000", "$3,000,000"],
            ["Film B", "$500,000", "$2,000,000"],
            ["Film C", "$2,000,000", "$3,000,000"]
        ])
        
        result = links.most_profitable(2)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_longest(self, sample_data, mocker):
        links_path, movies_path = sample_data
        links = Links(links_path, movies_path)
        
        mocker.patch.object(Links, 'get_imdb', return_value=[
            ["Film A", None, None, "120 min"],
            ["Film B", None, None, "90 min"],
            ["Film C", None, None, "180 min"]
        ])
        
        result = links.longest(2)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_top_cost_per_minute(self, sample_data, mocker):
        links_path, movies_path = sample_data
        links = Links(links_path, movies_path)
        
        mocker.patch.object(Links, 'get_imdb', return_value=[
            ["Film A", "$1,000,000", None, "100 min"],
            ["Film B", "$500,000", None, "50 min"],
            ["Film C", "$900,000", None, "100 min"]
        ])
        
        result = links.top_cost_per_minute(2)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, (int, float)) for v in result.values())
        # Проверка сортировки
        values = list(result.values())
        assert values == sorted(values, reverse=True)

class TestRatingsExtended:
    @pytest.fixture
    def sample_data(self, tmp_path):
        ratings_data = [
            {"userId": "1", "movieId": "1", "rating": "5.0", "timestamp": "1000"},
            {"userId": "1", "movieId": "2", "rating": "3.5", "timestamp": "1001"},
            {"userId": "2", "movieId": "1", "rating": "4.5", "timestamp": "1002"},
            {"userId": "2", "movieId": "3", "rating": "2.0", "timestamp": "1003"},
            {"userId": "3", "movieId": "1", "rating": "3.0", "timestamp": "1004"},
        ]
        movies_data = [
            {"movieId": "1", "title": "Film A", "genres": "Action"},
            {"movieId": "2", "title": "Film B", "genres": "Comedy"},
            {"movieId": "3", "title": "Film C", "genres": "Drama"},
        ]
        
        ratings_path = tmp_path / "ratings.csv"
        movies_path = tmp_path / "movies.csv"
        
        with open(ratings_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["userId", "movieId", "rating", "timestamp"])
            writer.writeheader()
            writer.writerows(ratings_data)
            
        with open(movies_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["movieId", "title", "genres"])
            writer.writeheader()
            writer.writerows(movies_data)
            
        return ratings_path, movies_path

    # Movies sub-class tests
    def test_movies_dist_by_rating(self, sample_data):
        ratings_path, movies_path = sample_data
        ratings = Ratings(ratings_path, movies_path)
        movies = ratings.Movies(ratings)
        result = movies.dist_by_rating()
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, float) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки (по ключам)
        keys = list(result.keys())
        assert keys == sorted(keys)

    def test_movies_top_by_num_of_ratings(self, sample_data):
        ratings_path, movies_path = sample_data
        ratings = Ratings(ratings_path, movies_path)
        movies = ratings.Movies(ratings)
        result = movies.top_by_num_of_ratings(2)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_movies_top_by_ratings_avg(self, sample_data):
        ratings_path, movies_path = sample_data
        ratings = Ratings(ratings_path, movies_path)
        movies = ratings.Movies(ratings)
        result = movies.top_by_ratings(2, metric='average')
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, float) for v in result.values())
        # Проверка сортировки
        ratings = list(result.values())
        assert ratings == sorted(ratings, reverse=True)

    def test_movies_top_controversial(self, sample_data):
        ratings_path, movies_path = sample_data
        ratings = Ratings(ratings_path, movies_path)
        movies = ratings.Movies(ratings)
        result = movies.top_controversial(2)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, float) for v in result.values())
        # Проверка сортировки
        variances = list(result.values())
        assert variances == sorted(variances, reverse=True)

    # Users sub-class tests
    def test_users_dist_by_num_of_ratings(self, sample_data):
        ratings_path, movies_path = sample_data
        ratings = Ratings(ratings_path, movies_path)
        users = ratings.Users(ratings)
        result = users.dist_by_num_of_ratings()
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_users_dist_by_avg(self, sample_data):
        ratings_path, movies_path = sample_data
        ratings = Ratings(ratings_path, movies_path)
        users = ratings.Users(ratings)
        result = users.dist_by_avg_or_median(metric='average')
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, float) for v in result.values())
        # Проверка сортировки (по возрастанию)
        avgs = list(result.values())
        assert avgs == sorted(avgs)

    def test_users_top_controversial(self, sample_data):
        ratings_path, movies_path = sample_data
        ratings = Ratings(ratings_path, movies_path)
        users = ratings.Users(ratings)
        result = users.top_controversial_users(2)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, float) for v in result.values())
        # Проверка сортировки
        variances = list(result.values())
        assert variances == sorted(variances, reverse=True)

class TestTagsExtended:
    @pytest.fixture
    def sample_data(self, tmp_path):
        data = [
            {"userId": "1", "movieId": "1", "tag": "exciting action", "timestamp": "1000"},
            {"userId": "1", "movieId": "2", "tag": "funny comedy", "timestamp": "1001"},
            {"userId": "2", "movieId": "1", "tag": "thrilling experience", "timestamp": "1002"},
            {"userId": "3", "movieId": "3", "tag": "emotional drama", "timestamp": "1003"},
            {"userId": "2", "movieId": "2", "tag": "hilarious moments", "timestamp": "1004"},
            {"userId": "3", "movieId": "1", "tag": "action-packed adventure", "timestamp": "1005"},
        ]
        path = tmp_path / "tags.csv"
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["userId", "movieId", "tag", "timestamp"])
            writer.writeheader()
            writer.writerows(data)
        return path

    def test_most_words(self, sample_data):
        tags = Tags(sample_data)
        result = tags.most_words(3)
        
        # Проверка типа
        assert isinstance(result, list)
        # Проверка типов элементов
        assert all(isinstance(item, str) for item in result)
        # Проверка сортировки (по количеству слов)
        word_counts = [len(tag.split()) for tag in result]
        assert word_counts == sorted(word_counts, reverse=True)

    def test_longest(self, sample_data):
        tags = Tags(sample_data)
        result = tags.longest(3)
        
        # Проверка типа
        assert isinstance(result, list)
        # Проверка типов элементов
        assert all(isinstance(item, str) for item in result)
        # Проверка сортировки (по длине строки)
        lengths = [len(tag) for tag in result]
        assert lengths == sorted(lengths, reverse=True)

    def test_most_words_and_longest(self, sample_data):
        tags = Tags(sample_data)
        result = tags.most_words_and_longest(3)
        
        # Проверка типа
        assert isinstance(result, list)
        # Проверка типов элементов
        assert all(isinstance(item, str) for item in result)
        # Проверка сортировки (алфавитная)
        assert result == sorted(result)

    def test_most_popular(self, sample_data):
        tags = Tags(sample_data)
        result = tags.most_popular(3)
        
        # Проверка типа
        assert isinstance(result, dict)
        # Проверка типов элементов
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        # Проверка сортировки
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_tags_with(self, sample_data):
        tags = Tags(sample_data)
        result = tags.tags_with("action")
        
        # Проверка типа
        assert isinstance(result, list)
        # Проверка типов элементов
        assert all(isinstance(item, str) for item in result)
        # Проверка сортировки (алфавитная)
        assert result == sorted(result)
