
def get_click_tile(click, render_coof,map):
    '''
    Функция, определяющая, по какому тайлу кликнули мышью.
    Клик за пределами сцены не учитывается
    '''
    cor = [click[0]-render_coof[0],click[1]-render_coof[1]]
    x = 0
    y = 0
    while cor[0] >100:
        cor[0] -= 100
        x+=1
    while cor[1] >100:
        cor[1] -= 100
        y+=1
    if cor[0] >= 0 and cor[1] >= 0 and x < len(map[0]) and y < len(map):
        return (x,y)
    else:
        return -1