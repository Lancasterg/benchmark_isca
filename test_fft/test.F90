program test

call time_fft()






contains

subroutine time_fft()
use fft_mod

integer :: lot
real(kind=8)   , allocatable :: ain(:,:), aout(:,:)
complex(kind=8), allocatable :: four(:,:)
integer :: i, j, m, n, k, h, iter
integer :: ntrans(4) = (/ 64 ,128, 256, 512 /)
integer :: lots(4) = (/32, 64, 128, 256 /)
real :: start_time = 0, stop_time = 0, mean_time_iter = 0, mean_time_full = 0, append_time = 0
real :: time_3d_start = 0, time_3d_stop = 0
iter = 100

! test multiple transform lengths
  do m = 1, 4

  ! set up input data
    n = ntrans(m)
    lot = lots(m)

    allocate(ain(n+1,lot),aout(n+1,lot),four(n/2+1,lot))

    call fft_init(n)

    do k = 1, iter
        call random_number(ain(1:n,:))
        four = fft_grid_to_fourier(ain)
        call cpu_time(start_time)
            aout = fft_fourier_to_grid(four)
        call cpu_time(stop_time)
        append_time = append_time + (stop_time - start_time)
    enddo

    mean_time_iter = append_time / iter

    append_time = 0.0
    start_time = 0.0
    stop_time = 0.0

    do k = 1, iter
        call random_number(ain(1:n,:))
        four = fft_grid_to_fourier(ain)
        call cpu_time(time_3d_start)
        do h = 1, 25
            aout = fft_fourier_to_grid(four)
        enddo
        call cpu_time(time_3d_stop)
        append_time = append_time + (time_3d_stop - time_3d_start)
    enddo

    mean_time_full = append_time / iter

    ! aout = fft_fourier_to_grid (four)

    call fft_end()
    deallocate (ain,aout,four)


    print *, '( ',n,' x ' ,lot ,' ), mean_iteration_time: '
    write (*,'(f15.9)') mean_time_iter
    print *, '( ',n,' x ' ,lot ,' ), mean_full_time: '
    write (*,'(f15.9)') mean_time_full

    print *, '------------------------------------------------------------'
 enddo

end subroutine time_fft

end program test
