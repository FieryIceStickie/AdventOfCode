program main
   implicit none
   integer :: f
   integer :: ios
   integer :: i, j, k, v
   character(len=100) :: line
   integer, dimension(41, 41) :: grid

   type :: coord
      integer :: x
      integer :: y
   end type

   type :: list
      type(coord), dimension(41*41) :: elems
      integer :: size
   end type

   type(list) :: zeroes

   integer :: p1, p2
   type(list) :: bfs, nines
   type(coord) :: start, z, d, loc
   type(coord), dimension(4) :: deltas
   integer :: h
   h = 41
   deltas = [coord(-1, 0), coord(0, 1), coord(1, 0), coord(0, -1)]
   p1 = 0
   p2 = 0

   open (newunit=f, file='input.txt', status='old', action='read', iostat=ios)
   i = 1
   do
      read (unit=f, fmt='(a)', iostat=ios) line
      if (ios /= 0) exit
      j = 1
      do
         if (j > h) exit
         read (line(j:j), *) v
         if (v == 0) then
            call append(zeroes, coord(i, j))
         end if
         grid(i, j) = v
         j = j + 1
      end do
      i = i + 1
   end do
   close (f)

   i = 1
   do
      if (i > zeroes%size) exit
      start = zeroes%elems(i)

      bfs%size = 0
      call append(bfs, start)
      nines%size = 0
      j = 1
      do
         if (j > bfs%size) exit
         z = bfs%elems(j)

         if (grid_get(z) == 9) then
            p2 = p2 + 1
            if (.not. in(nines, z)) call append(nines, z)
         else
            k = 1
            do
               if (k > 4) exit
               d = deltas(k)
               loc = add(z, d)
               if (within(loc) .and. grid_get(loc) == grid_get(z) + 1) call append(bfs, loc)
               k = k + 1
            end do
         end if
         j = j + 1
      end do
      p1 = p1 + nines%size
      i = i + 1
   end do
   print *, p1, p2

contains
   logical function within(pos)
      type(coord), intent(in) :: pos
      within = 1 <= pos%x .and. pos%x <= h .and. 1 <= pos%y .and. pos%y <= h
   end function within

   type(coord) function add(v1, v2)
      type(coord), intent(in) :: v1, v2
      add = coord(v1%x + v2%x, v1%y + v2%y)
   end function add

   integer function grid_get(pos)
      type(coord), intent(in) :: pos
      grid_get = grid(pos%x, pos%y)
   end function grid_get

   logical function eq(z1, z2)
      type(coord), intent(in) :: z1, z2
      eq = z1%x == z2%x .and. z1%y == z2%y
   end function eq

   logical function in(arr, item)
      type(list), intent(in) :: arr
      type(coord), intent(in) :: item
      integer :: idx

      idx = 1
      do
         if (idx > arr%size) exit
         if (eq(arr%elems(idx), item)) then
            in = .true.
            return
         end if
         idx = idx + 1
      end do
      in = .false.
   end function in

   subroutine append(arr, item)
      type(list), intent(inout) :: arr
      type(coord), intent(in) :: item
      arr%size = arr%size + 1
      arr%elems(arr%size) = item
   end subroutine append
end
