# Battleship Game

## Spis treści

1. [Wstęp](#wstęp)
2. [Struktura plików](#struktura-plików)
3. [Instrukcja uruchomienia](#instrukcja-uruchomienia)
4. [Moduły](#moduły)
    - [main.py](#mainpy)
    - [menu.py](#menupy)
    - [ship.py](#shippy)
    - [ship_manager.py](#ship_managerpy)
    - [game_board.py](#game_boardpy)
    - [fire_animation.py](#fire_animationpy)
    - [slider.py](#sliderpy)
    - [button.py](#buttonpy)

## Wstęp

Gra w statki to popularna gra planszowa, w której gracze rozmieszczają swoje statki na planszy i na przemian próbują trafiać statki przeciwnika. Poniższa dokumentacja opisuje strukturę plików, instrukcje uruchomienia oraz szczegóły dotyczące modułów i klas w projekcie.

# Struktura projektu Battleship

## assets/
Zasoby używane w grze, takie jak obrazy, dźwięki i animacje.

### menu/
- `Battleship.png`

### ships/
Obrazy statków, podzielone na różne typy statków.

#### carrier/
- `carrier.png`

#### cruiser/
- `cruiser.png`

#### destroyer/
- `destroyer.png`

#### patrolBoat/
- `patrolBoat.png`

#### submarine/
- `submarine.png`

### sounds/
Pliki dźwiękowe używane w grze.

- `click.mp3`
- `hit.wav`
- `miss.mp3`
- `music.mp3`

### token/
Obrazy używane do oznaczania trafień i chybionych strzałów.

- `hit.png`
- `miss.png`

### board/
Obraz planszy gry.

- `board.jpeg`

## main.py
Główny plik uruchamiający grę. Zawiera klasę `BattleshipGame` odpowiedzialną za uruchomienie gry, obsługę zdarzeń, rysowanie ekranu oraz zarządzanie stanem gry.

## menu.py
Moduł zarządzający menu głównym gry.

## ship.py
Moduł definiujący klasy statków.

## ship_manager.py
Moduł zarządzający statkami na planszy.

## game_board.py
Moduł zarządzający planszą gry.

## fire_animation.py
Moduł zarządzający animacją ognia.

## slider.py
Moduł zarządzający suwakiem do regulacji głośności.

## button.py
Moduł zarządzający przyciskami.


## Instrukcja uruchomienia

1. Upewnij się, że masz zainstalowane biblioteki Pygame.
   ```bash
   pip install pygame
   
2. Skopiuj wszystkie pliki do jednego folderu, zachowując strukturę katalogów assets.
3. Uruchom plik main.py.
   ```bash
   python main.py
   
## Moduły

### main.py

Główny plik uruchamiający grę. Zawiera klasę `BattleshipGame` odpowiedzialną za uruchomienie gry, obsługę zdarzeń, rysowanie ekranu oraz zarządzanie stanem gry.

#### BattleshipGame

- **`__init__(self)`**: Inicjalizuje grę, ładuje zasoby, tworzy obiekty gry.
- **`computer_turn(self)`**: Realizuje ruch komputera.
- **`check_game_over(self)`**: Sprawdza, czy gra się zakończyła.
- **`reset_game(self, winner_message="", winner_color=(255, 255, 255))`**: Resetuje stan gry.
- **`handle_events(self, current_time)`**: Obsługuje zdarzenia użytkownika.
- **`handle_pre_game_events(self, event)`**: Obsługuje zdarzenia przed rozpoczęciem gry.
- **`handle_in_game_events(self, event, current_time)`**: Obsługuje zdarzenia podczas gry.
- **`handle_shot_result(self, cell, current_time)`**: Obsługuje wynik strzału.
- **`update_game_state(self, current_time)`**: Aktualizuje stan gry.
- **`handle_game_over(self, player_lost, opponent_lost)`**: Obsługuje zakończenie gry.
- **`draw_screen(self)`**: Rysuje ekran gry.
- **`run(self)`**: Główna pętla gry.

### menu.py

Moduł zarządzający menu głównym gry.

#### Menu

- **`__init__(self, screen, image_path, start_button, exit_button)`**: Inicjalizuje menu główne.
- **`draw(self)`**: Rysuje menu główne.
- **`handle_event(self, event)`**: Obsługuje zdarzenia w menu.
- **`set_winner_message(self, message, color)`**: Ustawia komunikat zwycięzcy.

### ship.py

Moduł definiujący klasy statków.

#### Ship

- **`__init__(self, x, y, width, height, image_path)`**: Inicjalizuje statek.
- **`load_image(self)`**: Ładuje obrazek statku.
- **`draw(self, screen, hidden=False)`**: Rysuje statek.
- **`handle_event(self, event, game_board)`**: Obsługuje zdarzenia związane ze statkiem.
- **`reset_position(self)`**: Resetuje pozycję statku.
- **`rotate(self, game_board, reset=False)`**: Obraca statek.
- **`get_cells(self)`**: Pobiera komórki zajmowane przez statek.

#### PatrolBoat (Ship)

- **`__init__(self, x, y, cell_size)`**: Inicjalizuje statek typu PatrolBoat.

#### Cruiser (Ship)

- **`__init__(self, x, y, cell_size)`**: Inicjalizuje statek typu Cruiser.

#### Destroyer (Ship)

- **`__init__(self, x, y, cell_size)`**: Inicjalizuje statek typu Destroyer.

#### Submarine (Ship)

- **`__init__(self, x, y, cell_size)`**: Inicjalizuje statek typu Submarine.

#### Carrier (Ship)

- **`__init__(self, x, y, cell_size)`**: Inicjalizuje statek typu Carrier.

### ship_manager.py

Moduł zarządzający statkami na planszy.

#### ShipManager

- **`__init__(self, cell_size)`**: Inicjalizuje menedżera statków.
- **`create_ships(self)`**: Tworzy statki.
- **`draw(self, screen, hidden=False)`**: Rysuje statki.
- **`handle_event(self, event, game_board, game_started)`**: Obsługuje zdarzenia związane ze statkami.
- **`randomize_ships(self, game_board)`**: Losowo rozmieszcza statki na planszy.
- **`all_ships_placed(self)`**: Sprawdza, czy wszystkie statki są rozmieszczone.
- **`is_hit(self, cell)`**: Sprawdza, czy statek został trafiony.
- **`get_all_ship_cells(self)`**: Pobiera wszystkie komórki zajmowane przez statki.

### game_board.py

Moduł zarządzający planszą gry.

#### GameBoard

- **`__init__(self, rows, cols, cell_size, pos)`**: Inicjalizuje planszę gry.
- **`create_grid(self)`**: Tworzy siatkę planszy.
- **`draw(self, screen)`**: Rysuje planszę.
- **`draw_hits(self, screen, hit_image, miss_image, is_player_board)`**: Rysuje trafienia na planszy.
- **`draw_fire_animations(self, screen)`**: Rysuje animacje ognia na planszy.
- **`get_cell(self, x, y)`**: Pobiera komórkę na podstawie współrzędnych.
- **`add_ship(self, ship)`**: Dodaje statek do planszy.
- **`remove_ship(self, ship)`**: Usuwa statek z planszy.
- **`ship_fits(self, ship, top_left_cell)`**: Sprawdza, czy statek mieści się na planszy.
- **`adjust_ship_position(self, ship)`**: Dopasowuje pozycję statku na planszy.
- **`reset_occupied_cells(self)`**: Resetuje zajęte komórki.
- **`select_cell(self, x, y, opponent, is_player_board)`**: Wybiera komórkę na planszy.
- **`is_hit(self, cell)`**: Sprawdza, czy komórka została trafiona.

### fire_animation.py

Moduł zarządzający animacją ognia.

#### FireAnimation

- **`__init__(self, cell_size)`**: Inicjalizuje animację ognia.
- **`load_frames(self)`**: Ładuje klatki animacji.
- **`start(self, position)`**: Uruchamia animację.
- **`update(self)`**: Aktualizuje animację.
- **`draw(self, screen)`**: Rysuje animację.

### slider.py

Moduł zarządzający suwakiem do regulacji głośności.

#### Slider

- **`__init__(self, x, y, width, height, min_val=0, max_val=1, initial_val=0.5)`**: Inicjalizuje suwak.
- **`draw(self, screen)`**: Rysuje suwak.
- **`handle_event(self, event)`**: Obsługuje zdarzenia związane z suwakiem.
- **`get_value(self)`**: Pobiera wartość suwaka.

### button.py

Moduł zarządzający przyciskami.

#### Button

- **`__init__(self, x, y, width, height, text)`**: Inicjalizuje przycisk.
- **`draw(self, screen)`**: Rysuje przycisk.
- **`is_clicked(self, event)`**: Sprawdza, czy przycisk został kliknięty.

